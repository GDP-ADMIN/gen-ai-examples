"""Helper module.

This module contains helper functions for the FastAPI application.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Dimitrij Ray (dimitrij.ray@gdplabs.id)

References:
    None
"""

from enum import StrEnum
from typing import Any

from gllm_retrieval.reranker.reranker import BaseReranker

from claudia_gpt.config.constant import COHERE_API_KEY, COHERE_MODEL
from claudia_gpt.config.schemas.reranker_schema import CohereRerankerConfig
from claudia_gpt.reranker.cohere_reranker import CohereReranker
from claudia_gpt.reranker.no_op_reranker import NoOpReranker


class RerankerType(StrEnum):
    """The type of reranker.

    Values:
        FLAG_EMBEDDING: The flag embedding reranker.
        COHERE: The Cohere reranker.
        NO_OP: The no-op reranker.
    """

    FLAG_EMBEDDING = "flag_embedding"
    COHERE = "cohere"
    NO_OP = "no_op"


# Custom implementation for Claudia
def get_reranker(type: RerankerType, **kwargs: Any) -> BaseReranker | None:  # noqa: ARG001
    """Get reranker based on keyword arguments.

    Args:
        type (RerankerType): The type of reranker.
        kwargs (Any): The keyword arguments.

    Returns:
        BaseReranker | None : The reranker.
    """
    if type == RerankerType.COHERE:
        return CohereReranker(CohereRerankerConfig(api_key=COHERE_API_KEY, model=COHERE_MODEL))

    if type == RerankerType.NO_OP:
        return NoOpReranker()

    return None
