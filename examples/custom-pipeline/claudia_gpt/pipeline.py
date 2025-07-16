"""Claudia Pipeline Configuration.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

import json
from typing import Any

from dotenv import load_dotenv
from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from gllm_datastore.vector_data_store import ElasticsearchVectorDataStore
from gllm_generation.response_synthesizer import StuffResponseSynthesizer
from gllm_inference.multimodal_lm_invoker import OpenAIMultimodalLMInvoker
from gllm_inference.prompt_builder import OpenAIPromptBuilder
from gllm_inference.request_processor import LMRequestProcessor
from gllm_misc.context_manipulator.repacker.repacker import Repacker, RepackerMode
from gllm_pipeline.pipeline.pipeline import Pipeline
from gllm_pipeline.steps import bundle, step, toggle, transform
from gllm_pipeline.steps.pipeline_step import BasePipelineStep
from gllm_plugin.pipeline.pipeline_plugin import PipelineBuilderPlugin
from gllm_retrieval.reranker.reranker import BaseReranker
from gllm_retrieval.retriever.vector_retriever.basic_vector_retriever import BasicVectorRetriever
from langchain_openai import OpenAIEmbeddings
from pydantic import SecretStr

from claudia_gpt.component.catapa_query_transformer import CatapaQueryTransformer
from claudia_gpt.component.chat_history_manager import ChatHistoryManager
from claudia_gpt.config.constant import (
    DB_URL,
    DEFAULT_MODEL,
    ELASTICSEARCH_INDEX_NAME,
    ELASTICSEARCH_URL,
    HELP_CENTER_USE_CASE_SYSTEM_PROMPT,
    HELP_CENTER_USE_CASE_USER_PROMPT,
    OPENAI_API_KEY,
    OPENAI_EMBEDDING_MODEL,
)
from claudia_gpt.config.pipeline.general_pipeline_config import GeneralPipelineConfigKeys
from claudia_gpt.config.pipeline.pipeline_helper import build_save_history_step
from claudia_gpt.config.supported_models import ModelName
from claudia_gpt.constant.agent_type import AgentType
from claudia_gpt.preset_config import ClaudiaPresetConfig
from claudia_gpt.runtime_config import ClaudiaRuntimeConfig, ClaudiaRuntimeConfigKeys
from claudia_gpt.runtime_config import ClaudiaRuntimeConfigKeys as ConfigKeys
from claudia_gpt.state import ClaudiaState, ClaudiaStateKeys, create_initial_state
from claudia_gpt.utils.initializer import (
    RerankerType,
    get_chat_history_storage,
    get_reranker,
)

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
        self.data_store = SQLAlchemySQLDataStore(engine_or_url=DB_URL, pool_pre_ping=True)

    async def build(self, pipeline_config: dict[str, Any]) -> Pipeline:
        """Build the pipeline.

        Args:
            pipeline_config (dict[str, Any]): The pipeline configuration.

        Returns:
            Pipeline: The simple pipeline.
        """
        # Query Transformer
        optional_catapa_query_transformer_step = self._build_optional_catapa_query_transformer_step()

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
            input_state_map={"chunks": ClaudiaStateKeys.CHUNKS},
            output_state=ClaudiaStateKeys.CONTEXT,
        )

        # Bundler
        bundler_step = bundle(
            input_states=[ClaudiaStateKeys.CONTEXT],
            output_state=ClaudiaStateKeys.RESPONSE_SYNTHESIS_BUNDLE,
        )

        # Resposne Synthesizer
        response_synthesizer_step = self._build_catapa_response_synthesizer_step()

        # Save Message Step
        anonymizer_storage = None
        chat_history_storage = get_chat_history_storage()
        chat_history_manager = ChatHistoryManager(storage=chat_history_storage, anonymizer_storage=anonymizer_storage)
        save_history_step = build_save_history_step(
            chat_history_manager=chat_history_manager,
            name="save_history",
            additional_input_state_map={
                ChatHistoryManager.QUERY_KEY: ClaudiaStateKeys.USER_QUERY,
                ChatHistoryManager.NEW_ANONYMIZED_MAPPINGS_KEY: ClaudiaStateKeys.NEW_ANONYMIZED_MAPPINGS,
                ChatHistoryManager.REFERENCES_KEY: ClaudiaStateKeys.REFERENCES,
                ChatHistoryManager.AGENT_TYPE_KEY: ClaudiaStateKeys.AGENT_TYPE,
                ChatHistoryManager.AGENT_IDS_KEY: ClaudiaStateKeys.AGENT_IDS,
            },
            additional_runtime_config_map={
                ChatHistoryManager.SEARCH_TYPE_KEY: GeneralPipelineConfigKeys.SEARCH_TYPE,
                ChatHistoryManager.ANONYMIZE_EM_KEY: GeneralPipelineConfigKeys.ANONYMIZE_EM,
                ChatHistoryManager.ANONYMIZE_LM_KEY: GeneralPipelineConfigKeys.ANONYMIZE_LM,
            },
        )

        return Pipeline(
            steps=[
                optional_catapa_query_transformer_step,
                catapa_retriever_step,
                optional_rerank_chunks_step,
                limit_chunks_step,
                repacker_step,
                bundler_step,
                response_synthesizer_step,
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
                "chunks": ClaudiaStateKeys.CHUNKS,
                "query": ClaudiaStateKeys.TRANSFORMED_QUERY,
            },
            output_state=ClaudiaStateKeys.CHUNKS,
        )

        return toggle(
            name="rerank_chunks",
            condition=lambda input: input["rerank_type"] != "none",
            if_branch=rerank_step,
            input_state_map={
                "chunks": ClaudiaStateKeys.CHUNKS,
                "query": ClaudiaStateKeys.TRANSFORMED_QUERY,
            },
            runtime_config_map={
                ClaudiaRuntimeConfigKeys.RERANK_KWARGS: ConfigKeys.RERANK_KWARGS,
                ClaudiaRuntimeConfigKeys.RERANK_TYPE: ConfigKeys.RERANK_TYPE,
            },
        )

    def _build_limit_chunks_step(self) -> BasePipelineStep:
        """Build the limit chunks step.

        Returns:
            BasePipelineStep: The limit chunks step that selects top n chunks.
        """
        return transform(
            operation=lambda inputs: inputs["chunks"][: self.CHUNK_LIMIT],
            input_states=[ClaudiaStateKeys.CHUNKS],
            output_state=ClaudiaStateKeys.CHUNKS,
        )

    def _build_optional_catapa_query_transformer_step(self) -> BasePipelineStep:
        """Build the optional flag embedding chunks step.

        Returns:
            BasePipelineStep: The optional flag embedding rerank chunks step.
        """
        query_transformer_step = step(
            component=CatapaQueryTransformer(),
            input_state_map={
                CatapaQueryTransformer.QUERY_KEY: ClaudiaStateKeys.USER_QUERY,
                CatapaQueryTransformer.CHAT_HISTORY_KEY: ClaudiaStateKeys.HISTORY,
            },
            output_state=ClaudiaStateKeys.TRANSFORMED_QUERY,
        )

        return toggle(
            name="catapa_query_transformer",
            condition=lambda input: input["agent_type"] == AgentType.HELP_CENTER_CATAPA.value,
            if_branch=query_transformer_step,
            input_state_map={
                CatapaQueryTransformer.QUERY_KEY: ClaudiaStateKeys.USER_QUERY,
                CatapaQueryTransformer.CHAT_HISTORY_KEY: ClaudiaStateKeys.HISTORY,
            },
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
                "query": ClaudiaStateKeys.TRANSFORMED_QUERY,
                "retrieval_params": ClaudiaStateKeys.RETRIEVAL_PARAMS,
            },
            output_state=ClaudiaStateKeys.CHUNKS,
            fixed_args={"top_k": pipeline_config.get(ConfigKeys.NORMAL_SEARCH_TOP_K)},
        )
        return catapa_retriever_step

    def _build_catapa_response_synthesizer_step(self) -> BasePipelineStep:
        """Build the optional CATAPA response synthesizer step.

        Returns:
            BasePipelineStep: The optional CATAPA response synthesizer step.
        """
        model_name = ModelName.from_string(DEFAULT_MODEL)
        final_model_name = model_name.get_full_name()
        prompt_builder = OpenAIPromptBuilder(HELP_CENTER_USE_CASE_SYSTEM_PROMPT, HELP_CENTER_USE_CASE_USER_PROMPT)
        lm_invoker = OpenAIMultimodalLMInvoker(
            model_name=final_model_name,
            api_key=OPENAI_API_KEY,
            default_hyperparameters={"temperature": 0.0},
        )
        lm_request_processor = LMRequestProcessor(prompt_builder, lm_invoker)
        response_synthesizer = StuffResponseSynthesizer(lm_request_processor)
        response_synthesizer_step = step(
            component=response_synthesizer,
            input_state_map={
                "query": ClaudiaStateKeys.TRANSFORMED_QUERY,
                "state_variables": ClaudiaStateKeys.RESPONSE_SYNTHESIS_BUNDLE,
                "history": ClaudiaStateKeys.HISTORY,
                "event_emitter": ClaudiaStateKeys.EVENT_EMITTER,
            },
            output_state=ClaudiaStateKeys.RESPONSE,
        )
        return response_synthesizer_step

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

        embedding_model = OpenAIEmbeddings(model=OPENAI_EMBEDDING_MODEL, openai_api_key=SecretStr(OPENAI_API_KEY))
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
