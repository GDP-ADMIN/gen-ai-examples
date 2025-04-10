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
        response_synthesis_bundle (dict[str, Any]): The bundle of response synthesis.
        response (str): The generated response to the user's query.
    """

    response_synthesis_bundle: dict[str, Any]
    response: str


class SimpleStateKeys(StrEnum):
    """List of all possible keys in SimpleState."""

    RESPONSE_SYNTHESIS_BUNDLE = "response_synthesis_bundle"
    RESPONSE = "response"
