"""State for MCP Pipeline.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

from enum import StrEnum
from typing import TypedDict, Any

from gllm_core.event import EventEmitter

class McpState(TypedDict):
    """A TypedDict representing the state of the MCP Pipeline.

    Attributes:
        query (str): The user's query.
        response (str): The generated response to the user's query.
        history (Any): The chat history of the conversation.
        event_emitter (EventEmitter): The event emitter for handling events during response synthesis.
    """

    query: str
    response: str
    history: Any
    event_emitter: EventEmitter


class McpStateKeys(StrEnum):
    """List of all possible keys in McpState."""

    QUERY = "query"
    RESPONSE = "response"
    HISTORY = "history"
    EVENT_EMITTER = "event_emitter"
