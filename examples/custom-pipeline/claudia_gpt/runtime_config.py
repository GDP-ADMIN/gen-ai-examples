"""CATAPA RAG Pipeline Runtime Config.

Authors:
    Winson Evangelis Sutanto (winson.e.sutanto@gdplabs.id)
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

from enum import StrEnum

from pydantic import BaseModel


class ClaudiaRuntimeConfig(BaseModel):
    """A Pydantic model representing the runtime config of a CATAPA RAG pipeline.

    Attributes:
        rerank_kwargs (str): The keyword arguments for reranking.
        rerank_type (str): The type of reranking.
    """

    rerank_kwargs: str = ""
    rerank_type: str = ""


class ClaudiaRuntimeConfigKeys(StrEnum):
    """List of all possible keys in ClaudiaRuntimeConfig.

    Attributes:
        RERANK_KWARGS (str): The key for rerank kwargs.
        RERANK_TYPE (str): The key for rerank type.
    """

    RERANK_KWARGS = "rerank_kwargs"
    RERANK_TYPE = "rerank_type"
