"""Simple Pipeline State.

Authors:
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)

References:
    NONE
"""

from enum import StrEnum
from typing import Any, TypedDict

from gllm_core.event.event_emitter import EventEmitter


class SimpleState(TypedDict):
    """A TypedDict representing the state of a Simple pipeline.

    Attributes:
        event_emitter (EventEmitter): An event emitter instance.
        response_synthesis_bundle (dict[str, Any]): The bundle of response synthesis.
        response (str): The generated response to the user's query.
    """

    event_emitter: EventEmitter
    response_synthesis_bundle: dict[str, Any]
    response: str


class SimpleStateKeys(StrEnum):
    """List of all possible keys in SimpleState."""

    EVENT_EMITTER = "event_emitter"
    RESPONSE_SYNTHESIS_BUNDLE = "response_synthesis_bundle"
    RESPONSE = "response"
