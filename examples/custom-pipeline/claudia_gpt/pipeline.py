"""Claudia Pipeline Configuration.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

import json
from typing import Any

from dotenv import load_dotenv
from glchat_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore
from gllm_generation.reference_formatter import SimilarityBasedReferenceFormatter
from gllm_generation.response_synthesizer import StuffResponseSynthesizer
from gllm_inference.em_invoker import LangChainEMInvoker
from gllm_misc.context_manipulator.repacker.repacker import Repacker, RepackerMode
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import bundle, if_else, step, toggle, transform
from gllm_pipeline.steps.pipeline_step import BasePipelineStep
from gllm_retrieval.query_transformer import OneToOneQueryTransformer
from gllm_retrieval.query_transformer.query_transformer import ErrorHandling
from gllm_retrieval.reranker.reranker import BaseReranker
from gllm_retrieval.retriever.vector_retriever.basic_vector_retriever import BasicVectorRetriever
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from claudia_gpt.component.chat_history_manager import ChatHistoryManager
from claudia_gpt.config.constant import (
    DEFAULT_REFERENCE_FORMATTER_THRESHOLD,
    ELASTICSEARCH_INDEX_NAME,
    ELASTICSEARCH_URL,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
)
from claudia_gpt.config.pipeline.general_pipeline_config import GeneralPipelineConfigKeys
from claudia_gpt.config.pipeline.pipeline_helper import build_save_history_step, get_lmrp_by_scope, to_bool
from claudia_gpt.preset_config import ClaudiaPresetConfig
from claudia_gpt.runtime_config import ClaudiaRuntimeConfig
from claudia_gpt.runtime_config import ClaudiaRuntimeConfigKeys as ConfigKeys
from claudia_gpt.state import ClaudiaState, create_initial_state
from claudia_gpt.state import ClaudiaStateKeys as StateKeys
from claudia_gpt.utils.caching import is_prompt_within_context_limit
from claudia_gpt.utils.constant import chat_history_manager
from claudia_gpt.utils.initializer import (
    RerankerType,
    get_reranker,
)
from claudia_gpt.utils.prompts import assign_queries, concat_history_with_query, flatten_standalone_query

load_dotenv(override=True)


INDEX_NAME = "help_center_catapa"
HELP_CENTER_ELASTICSEARCH_INDEX_NAME = f"{ELASTICSEARCH_INDEX_NAME}_{INDEX_NAME}"


class ClaudiaPipelineBuilderPlugin(PipelineBuilderPlugin[ClaudiaState, ClaudiaPresetConfig]):
    """Claudia Pipeline Builder Plugin.

    Inherits attributes from `PipelineBuilderPlugin`.

    Attributes:
        CHUNK_LIMIT (int): The chunk limit.
        name (str): The name of the pipeline.
        additional_config_class (type[BaseModel]): The additional config class.
        preset_config_class (type[BaseModel]): The preset config class.
        data_store (SQLAlchemySQLDataStore): The data store.
    """

    CHUNK_LIMIT = 5
    name = "claudia-gpt"
    additional_config_class = ClaudiaRuntimeConfig
    preset_config_class = ClaudiaPresetConfig

    def __init__(self):
        """Initialize the Claudia pipeline builder."""
        super().__init__()

    async def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        # Retrieve History
        multimodality = to_bool(pipeline_config.get("support_multimodal", False))
        chat_history_limit = pipeline_config.get("chat_history_limit", 20)
        retrieve_history_step = self._build_retrieve_history_step(multimodality, chat_history_limit)

        # Query Transformer
        assign_queries_step = self._build_assign_queries_step()
        prompt_context_char_threshold = int(pipeline_config.get("prompt_context_char_threshold", 32000))
        combine_query_with_history_step = self._build_combine_query_with_history_step(prompt_context_char_threshold)
        build_standalone_query_step = self._build_standalone_query_step(prompt_context_char_threshold)

        # Retriever
        catapa_retriever_step = self._build_catapa_retriever_step(pipeline_config)

        # Reranker
        rerank_kwargs = json.loads(pipeline_config.get("rerank_kwargs", "{}") or "{}")
        rerank_type_string: str = pipeline_config.get("rerank_type", "no_op")
        rerank_type: RerankerType = RerankerType(rerank_type_string)
        rag_reranker = get_reranker(rerank_type, **rerank_kwargs)
        optional_rerank_chunks_step = self._build_optional_rerank_chunks_step(rag_reranker)

        # Limit Chunks
        limit_chunks_step = self._build_limit_chunks_step()

        # Repacker
        repacker_step = step(
            component=Repacker(mode=RepackerMode.CONTEXT.value),  # Custom implementation for claudia
            input_state_map={"chunks": StateKeys.CHUNKS},
            output_state=StateKeys.CONTEXT,
        )

        # Bundler
        bundler_step = bundle(
            input_states=[StateKeys.CONTEXT],
            output_state=StateKeys.RESPONSE_SYNTHESIS_BUNDLE,
        )

        # Resposne Synthesizer
        response_synthesizer_step = self._build_catapa_response_synthesizer_step()

        # Reference Fromatter
        reference_formatter_step = step(
            component=self.build_reference_formatter(),
            input_state_map={
                "response": "response",
                "chunks": "chunks",
                "event_emitter": "event_emitter",
            },
            output_state="references",
        )

        # Save Message Step
        save_history_step = build_save_history_step(
            chat_history_manager=chat_history_manager,
            name="save_history",
            additional_input_state_map={
                ChatHistoryManager.QUERY_KEY: StateKeys.USER_QUERY,
                ChatHistoryManager.NEW_ANONYMIZED_MAPPINGS_KEY: StateKeys.NEW_ANONYMIZED_MAPPINGS,
                ChatHistoryManager.REFERENCES_KEY: StateKeys.REFERENCES,
                ChatHistoryManager.RELATED_KEY: StateKeys.RELATED,
                ChatHistoryManager.STEP_INDICATORS_KEY: StateKeys.STEPS,
                ChatHistoryManager.MEDIA_MAPPING_KEY: StateKeys.MEDIA_MAPPING,
                ChatHistoryManager.CACHE_HIT_KEY: StateKeys.CACHE_HIT,
            },
            additional_runtime_config_map={
                ChatHistoryManager.SEARCH_TYPE_KEY: GeneralPipelineConfigKeys.SEARCH_TYPE,
                ChatHistoryManager.ANONYMIZE_EM_KEY: GeneralPipelineConfigKeys.ANONYMIZE_EM,
                ChatHistoryManager.ANONYMIZE_LM_KEY: GeneralPipelineConfigKeys.ANONYMIZE_LM,
            },
        )

        return Pipeline(
            steps=[
                retrieve_history_step,
                assign_queries_step,
                combine_query_with_history_step,
                build_standalone_query_step,
                catapa_retriever_step,
                optional_rerank_chunks_step,
                limit_chunks_step,
                repacker_step,
                bundler_step,
                response_synthesizer_step,
                reference_formatter_step,
                save_history_step,
            ],
            state_type=ClaudiaState,
        )

    def _build_optional_rerank_chunks_step(self, reranker: BaseReranker) -> BasePipelineStep:
        """Build the optional flag embedding chunks step.

        Returns:
            BasePipelineStep: The optional flag embedding rerank chunks step.
        """
        rerank_step = step(
            component=reranker,
            input_state_map={
                "chunks": StateKeys.CHUNKS,
                "query": StateKeys.STANDALONE_QUERY,
            },
            output_state=StateKeys.CHUNKS,
        )

        return toggle(
            name="rerank_chunks",
            condition=lambda input: input["rerank_type"] != "none",
            if_branch=rerank_step,
            input_state_map={
                "chunks": StateKeys.CHUNKS,
                "query": StateKeys.STANDALONE_QUERY,
            },
            runtime_config_map={
                "rerank_type": ConfigKeys.RERANK_TYPE,
            },
        )

    def _build_limit_chunks_step(self) -> BasePipelineStep:
        """Build the limit chunks step.

        Returns:
            BasePipelineStep: The limit chunks step that selects top n chunks.
        """
        return transform(
            operation=lambda inputs: inputs["chunks"][: self.CHUNK_LIMIT],
            input_states=[StateKeys.CHUNKS],
            output_state=StateKeys.CHUNKS,
        )

    def _build_retrieve_history_step(self, use_multimodal: bool, chat_history_limit: int) -> BasePipelineStep:
        """Build the retrieve history step.

        Args:
            use_multimodal (bool): The multimodal flag.
            chat_history_limit (int): The chat history limit.

        Returns:
            BasePipelineStep: The retrieve history step.
        """
        return step(
            component=chat_history_manager,
            input_state_map={},
            output_state=StateKeys.HISTORY,
            runtime_config_map={
                ChatHistoryManager.USER_ID_KEY: GeneralPipelineConfigKeys.USER_ID,
                ChatHistoryManager.CONVERSATION_ID_KEY: GeneralPipelineConfigKeys.CONVERSATION_ID,
                ChatHistoryManager.CHAT_HISTORY_KEY: GeneralPipelineConfigKeys.CHAT_HISTORY,
                ChatHistoryManager.LAST_MESSAGE_ID_KEY: GeneralPipelineConfigKeys.LAST_MESSAGE_ID,
            },
            fixed_args={
                ChatHistoryManager.OPERATION_KEY: ChatHistoryManager.OP_READ,
                ChatHistoryManager.IS_MULTIMODAL_KEY: use_multimodal,
                ChatHistoryManager.LIMIT_KEY: chat_history_limit,
            },
        )

    def _build_assign_queries_step(self) -> BasePipelineStep:
        """Build the assign queries step.

        Returns:
            BasePipelineStep: The assign queries step.
        """
        return transform(
            operation=assign_queries,
            input_states=[StateKeys.USER_QUERY, StateKeys.ANONYMIZED_QUERY],
            output_state=[StateKeys.RETRIEVAL_QUERY, StateKeys.GENERATION_QUERY],
            runtime_config_map={
                "anonymize_em": GeneralPipelineConfigKeys.ANONYMIZE_EM,
                "anonymize_lm": GeneralPipelineConfigKeys.ANONYMIZE_LM,
            },
        )

    def _build_combine_query_with_history_step(self, prompt_context_char_threshold: int) -> BasePipelineStep:
        """Build the combine query with history step.

        Includes the latest possible history messages without exceeding the prompt context character threshold.
        Only the latest messages that fit the threshold are included, in chronological order.

        Format:
            ```
            History:
            user: <user_message>
            assistant: <assistant_message>

            Query:
            <generation_query>
            ```

        Args:
            prompt_context_char_threshold (int): The character limit above which the prompt is assumed
            to have contained the context.

        Returns:
            BasePipelineStep: The combine query with history step.
        """
        return transform(
            operation=concat_history_with_query,
            input_states=[StateKeys.GENERATION_QUERY, StateKeys.HISTORY],
            output_state=StateKeys.JOINED_QUERY_WITH_HISTORY,
            name="combine_query_with_history",
            fixed_args={"prompt_context_char_threshold": prompt_context_char_threshold},
        )

    def _build_standalone_query_step(self, prompt_context_char_threshold: int) -> BasePipelineStep:
        """Build the standalone query step.

        Args:
            prompt_context_char_threshold (int): The character limit above which the prompt is assumed
            to have contained the context.

        Returns:
            BasePipelineStep: The standalone query step.
        """
        lmrp = get_lmrp_by_scope(self.lmrp_catalogs, "standard_rag_build_standalone_query", "openai")
        query_transformer = OneToOneQueryTransformer(
            lm_request_processor=lmrp,
            extract_func=lambda lm_output: lm_output.structured_output.get("transformed_query", ""),
            on_error=ErrorHandling.RAISE,
        )
        standalone_query_step = step(
            name="standalone_query_step",
            component=query_transformer,
            input_state_map={"query": StateKeys.JOINED_QUERY_WITH_HISTORY},
            output_state=StateKeys.STANDALONE_QUERY,
        )

        flatten_standalone_query_step = transform(
            operation=flatten_standalone_query,
            input_states=[StateKeys.STANDALONE_QUERY],
            output_state=StateKeys.STANDALONE_QUERY,
        )

        copy_query_to_standalone_query_step = transform(
            operation=lambda input: input[StateKeys.JOINED_QUERY_WITH_HISTORY],
            input_states=[StateKeys.JOINED_QUERY_WITH_HISTORY],
            output_state=StateKeys.STANDALONE_QUERY,
        )

        return if_else(
            name="standalone_query_toggle",
            condition=lambda input: (
                bool(input[StateKeys.HISTORY])
                and is_prompt_within_context_limit(
                    input[StateKeys.JOINED_QUERY_WITH_HISTORY],
                    prompt_context_char_threshold,
                )
            ),
            if_branch=[standalone_query_step, flatten_standalone_query_step],
            else_branch=copy_query_to_standalone_query_step,
        )

    def _build_catapa_retriever_step(self, pipeline_config: dict[str, Any]) -> BasePipelineStep:
        """Build the CATAPA retriever step.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            BasePipelineStep: The CATAPA retriever step.
        """
        catapa_retriever_step = step(
            component=self.build_retriever(HELP_CENTER_ELASTICSEARCH_INDEX_NAME),
            input_state_map={
                "query": StateKeys.STANDALONE_QUERY,
                "retrieval_params": StateKeys.RETRIEVAL_PARAMS,
            },
            output_state=StateKeys.CHUNKS,
            fixed_args={"top_k": pipeline_config.get("normal_search_top_k")},
        )
        return catapa_retriever_step

    def _build_catapa_response_synthesizer_step(self) -> BasePipelineStep:
        """Build the optional CATAPA response synthesizer step.

        Returns:
            BasePipelineStep: The optional CATAPA response synthesizer step.
        """
        lmrp = get_lmrp_by_scope(self.lmrp_catalogs, "help_center_response_synthesizer", "openai")
        response_synthesizer = StuffResponseSynthesizer(lmrp)
        response_synthesizer_step = step(
            component=response_synthesizer,
            input_state_map={
                "query": StateKeys.GENERATION_QUERY,
                "state_variables": StateKeys.RESPONSE_SYNTHESIS_BUNDLE,
                "history": StateKeys.HISTORY,
                "event_emitter": StateKeys.EVENT_EMITTER,
            },
            output_state=StateKeys.RESPONSE,
        )
        return response_synthesizer_step

    def build_reference_formatter(self) -> SimilarityBasedReferenceFormatter:
        """Build the reference formatter component.

        Returns:
            SimilarityBasedReferenceFormatter: The reference formatter component.
        """
        embedding_model = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=SecretStr(OPENAI_API_KEY))
        em_invoker = LangChainEMInvoker(em=embedding_model)
        return SimilarityBasedReferenceFormatter(
            em_invoker=em_invoker,
            threshold=DEFAULT_REFERENCE_FORMATTER_THRESHOLD,
            stringify=False,
        )

    def build_retriever(self, index_name: str) -> BasicVectorRetriever:
        """Build the retriever component.

        Args:
            index_name (str): The Elasticsearch index name.

        Returns:
            BasicVectorRetriever: The retriever component.

        Raises:
            ValueError: If the index name is not provided.
        """
        if not index_name:
            raise ValueError("Error building retriever. Index name must be provided.")

        embedding_model = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, api_key=SecretStr(OPENAI_API_KEY))
        data_store = ElasticsearchVectorDataStore(
            index_name=index_name, embedding=embedding_model, url=ELASTICSEARCH_URL
        )
        return BasicVectorRetriever(data_store)

    def build_initial_state(
        self, request_config: dict[str, Any], pipeline_config: dict[str, Any], **kwargs: Any
    ) -> ClaudiaState:
        """Build the initial state for pipeline invoke.

        Args:
            request_config (dict[str, Any]): The given request config from the user.
            pipeline_config (dict[str, Any]): The pipeline configuration.
            **kwargs (Any): A dictionary of arguments required for building the initial state.

        Returns:
            ClaudiaState: The initial state.
        """
        return create_initial_state(request_config, pipeline_config, **kwargs)
