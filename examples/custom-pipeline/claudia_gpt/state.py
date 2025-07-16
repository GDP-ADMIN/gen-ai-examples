"""State for Claudia Pipeline.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

from enum import StrEnum
from typing import Any, TypedDict

from gllm_core.event import EventEmitter


class ClaudiaState(TypedDict):
    """A TypedDict representing the state of the Claudia Pipeline.

    Attributes:
        query (str): The user's query.
        response (str): The generated response to the user's query.
        history (Any): The chat history of the conversation.
        event_emitter (EventEmitter): The event emitter for handling events during response synthesis.
        transformed_query (str): The transformed query.
        retrieval_params (Any): The retrieval parameters.
        chunks (Any): The chunks.
    """

    query: str
    response: str
    history: Any
    event_emitter: EventEmitter
    transformed_query: str
    retrieval_params: Any
    chunks: Any


class ClaudiaStateKeys(StrEnum):
    """List of all possible keys in ClaudiaState."""

    QUERY = "query"
    USER_QUERY = "user_query"
    TRANSFORMED_QUERY = "transformed_query"
    RESPONSE = "response"
    HISTORY = "history"
    EVENT_EMITTER = "event_emitter"
    RETRIEVAL_PARAMS = "retrieval_params"
    CHUNKS = "chunks"
    CHAT_HISTORY = "chat_history"
    CONTEXT = "context"
    RESPONSE_SYNTHESIS_BUNDLE = "response_synthesis_bundle"
    STATE_VARIABLES = "state_variables"
