"""State for Claudia Pipeline.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

import typing
from chunk import Chunk
from enum import StrEnum
from typing import Any, TypedDict

from gllm_core.event import EventEmitter

from claudia_gpt.anonymizer.schemas import AnonymizerMapping
from claudia_gpt.config.pipeline.pipeline_helper import get_retrieval_params


class ClaudiaState(TypedDict):
    """A TypedDict representing the state of a CATAPA Retrieval-Augmented Generation (RAG) pipeline.

    This docstring documents the original intention of each of the attributes in the TypedDict.
    However, in practice, the attributes may be modified or extended to suit the specific requirements of the
    application. The TypedDict is used to enforce the structure of the state object.

    Attributes:
        history (list[tuple[str, list[Any]]]): The history of the conversation or interaction.
        user_query (str): The original query from the user.
        queries (list[str]): A list of queries generated for retrieval.
        retrieval_params (dict[str, Any]): Parameters used for the retrieval process.
        chunks (list[Chunk]): A list of chunks retrieved from the knowledge base.
        graph_result (dict[str, Any]): The graph results from the graph retrieval process.
        graph_context (str): The context information from the graph retrieval process.
        context (str): The context information used for generating response.
        additional_instructions (str): Additional instructions sent to the language model.
        response_synthesis_bundle (dict[str, Any]): Data used for synthesizing the final response.
        response (str): The generated response to the user's query.
        anonymized_response (str): The anonymized version of the generated response.
        references (str | list[str] | list[Chunk]): References or sources used in generating the response.
        processed_urls (list[dict[str, Any]]): A list of processed URLs from user query.
        tenant (str | None): The tenant ID for the current request.
        agent_type (str): The type of agent used for the request.
        event_emitter (EventEmitter): An event emitter instance for logging purposes.
        new_anonymized_mappings (list[AnonymizerMapping]): The new anonymized mappings generated during the process.
        query_anonymized_data (dict[str, Any]): The anonymized data for the user query.
        context_anonymized_data (dict[str, Any]): The anonymized data for the context.
        response_anonymized_data (dict[str, Any]): The anonymized data for the response.
        agent_ids (list[str] | None): A list of agent IDs associated with the request.
        related (list[str]): The related topics or concepts.
        steps (list[dict[str, Any]]): The steps taken to generate response.
        media_mapping (dict[str, Any]): The media mapping.
        cache_hit (bool): The cache hit flag.
        generation_query (str): The query used for generation.
        joined_query_with_history (str): The query combined with the conversation history.
        standalone_query (str): The query combined with the conversation history.
        anonymized_query (str): The anonymized version of the user query.
        retrieval_query (str): The query used for retrieval.
    """

    history: list[tuple[str, list[Any]]]
    user_query: str
    queries: list[str]
    retrieval_params: dict[str, Any]
    chunks: list[Chunk]
    graph_result: dict[str, Any]
    graph_context: str
    context: str
    additional_instructions: str
    response_synthesis_bundle: dict[str, Any]
    response: str
    anonymized_response: str
    references: str | list[str] | list[Chunk]
    processed_urls: list[dict[str, Any]]
    tenant: str | None
    agent_type: str
    event_emitter: EventEmitter
    new_anonymized_mappings: list[AnonymizerMapping]
    query_anonymized_data: dict[str, Any]
    context_anonymized_data: dict[str, Any]
    response_anonymized_data: dict[str, Any]
    agent_ids: list[str] | None
    related: list[str]
    steps: list[dict[str, Any]]
    media_mapping: dict[str, Any]
    cache_hit: bool
    generation_query: str
    joined_query_with_history: str
    standalone_query: str
    anonymized_query: str
    retrieval_query: str


class ClaudiaStateKeys(StrEnum):
    """List of all possible keys in ClaudiaState."""

    USER_QUERY = "user_query"
    RESPONSE = "response"
    HISTORY = "history"
    EVENT_EMITTER = "event_emitter"
    RETRIEVAL_PARAMS = "retrieval_params"
    CHUNKS = "chunks"
    CHAT_HISTORY = "chat_history"
    CONTEXT = "context"
    RESPONSE_SYNTHESIS_BUNDLE = "response_synthesis_bundle"
    STATE_VARIABLES = "state_variables"
    NEW_ANONYMIZED_MAPPINGS = "new_anonymized_mappings"
    REFERENCES = "references"
    AGENT_TYPE = "agent_type"
    AGENT_IDS = "agent_ids"
    RELATED = "related"
    STEPS = "steps"
    MEDIA_MAPPING = "media_mapping"
    CACHE_HIT = "cache_hit"
    GENERATION_QUERY = "generation_query"
    JOINED_QUERY_WITH_HISTORY = "joined_query_with_history"
    STANDALONE_QUERY = "standalone_query"
    ANONYMIZED_QUERY = "anonymized_query"
    RETRIEVAL_QUERY = "retrieval_query"


def validate_state_completeness(state: ClaudiaState) -> None:
    """Validate that all required fields are present in the state.

    This function ensures that the factory function implements all fields
    defined in the ClaudiaState TypedDict.

    Args:
        state (ClaudiaState): The state to validate.

    Raises:
        ValueError: If any required fields are missing or unexpected fields are present.
    """
    required_fields = set(typing.get_type_hints(ClaudiaState).keys())
    actual_fields = set(state.keys())

    missing_fields = required_fields - actual_fields
    if missing_fields:
        raise ValueError(f"Missing required fields in state: {missing_fields}")

    extra_fields = actual_fields - required_fields
    if extra_fields:
        raise ValueError(f"Unexpected fields in state: {extra_fields}")


def create_initial_state(
    request_config: dict[str, Any], pipeline_config: dict[str, Any], **kwargs: Any
) -> ClaudiaState:
    """Create the initial state for pipeline invoke.

    Args:
        request_config (dict[str, Any]): The request.
        pipeline_config (dict[str, Any]): The pipeline configuration.
        **kwargs: Additional keyword arguments.

    Raises:
        ValueError: If any required fields are missing or unexpected fields are present.
        KeyError: If any required fields are missing in `request_config`.
    """
    event_emitter = kwargs["event_emitter"]
    if not isinstance(event_emitter, EventEmitter):
        raise ValueError("event_emitter must be an instance of EventEmitter")

    user_query = request_config["message"]
    if not isinstance(user_query, str):
        raise ValueError("user_query must be a string")

    initial_steps = kwargs["initial_steps"]
    if not isinstance(initial_steps, list):
        raise ValueError("initial_steps must be a list")

    for step in initial_steps:  # type: ignore[arg-type]
        if not isinstance(step, dict):
            raise ValueError("initial_steps must be a list of dictionaries")

    last_message_id = kwargs.get("last_message_id")
    if last_message_id is not None and not isinstance(last_message_id, str):
        raise ValueError("last_message_id must be a string")

    state = ClaudiaState(
        history=[],
        user_query=user_query,
        queries=[],
        retrieval_params=get_retrieval_params(request_config),
        chunks=[],
        graph_result={},
        graph_context="",
        context="",
        additional_instructions="",
        response_synthesis_bundle={},
        response="",
        anonymized_response="",
        references=[],
        processed_urls=[],
        tenant=None,
        agent_type="",
        event_emitter=event_emitter,
        new_anonymized_mappings=[],
        query_anonymized_data={},
        context_anonymized_data={},
        response_anonymized_data={},
        agent_ids=[],
        related=[],
        steps=initial_steps,  # type: ignore[arg-type]
        media_mapping={},
        cache_hit=False,
        generation_query="",
        joined_query_with_history="",
        standalone_query="",
        anonymized_query="",
        retrieval_query="",
    )

    validate_state_completeness(state)

    return state
