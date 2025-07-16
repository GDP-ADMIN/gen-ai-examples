"""CATAPA RAG Pipeline Runtime Config.

Authors:
    Winson Evangelis Sutanto (winson.e.sutanto@gdplabs.id)
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

from enum import StrEnum

from pydantic import BaseModel, Field


class ClaudiaRuntimeConfig(BaseModel):
    """A Pydantic model representing the runtime config of a CATAPA RAG pipeline.

    Attributes:
        normal_search_top_k (int): The top k for normal search. Must be greater than or equal to 1.
        rerank_kwargs (str): The keyword arguments for reranking.
        rerank_type (str): The type of reranking.
    """

    normal_search_top_k: int = Field(default=20, ge=1)
    rerank_kwargs: str = ""
    rerank_type: str = ""


class ClaudiaRuntimeConfigKeys(StrEnum):
    """List of all possible keys in ClaudiaRuntimeConfig.

    Attributes:
        NORMAL_SEARCH_TOP_K (str): The key for normal search top k.
        RERANK_KWARGS (str): The key for rerank kwargs.
        RERANK_TYPE (str): The key for rerank type.
    """

    NORMAL_SEARCH_TOP_K = "normal_search_top_k"
    RERANK_KWARGS = "rerank_kwargs"
    RERANK_TYPE = "rerank_type"
