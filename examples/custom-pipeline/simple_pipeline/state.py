"""Base Pipeline Preset Config.

Authors:
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

References:
    NONE
"""

from typing import TypedDict
from enum import StrEnum

from gllm_core.event.event_emitter import EventEmitter


class SimpleState(TypedDict):
    """A TypedDict representing the state of the Simple Pipeline.

    Attributes:
        query (str): The user's query.
        response (str): The generated response to the user's query.
    """

    query: str
    response: str
    event_emitter: EventEmitter



class SimpleStateKeys(StrEnum):
    """List of all possible keys in SimpleState."""

    QUERY = "query"
    RESPONSE = "response"
    EVENT_EMITTER = "event_emitter"
