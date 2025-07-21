"""Reranker module for no-op reranker.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)

References:
    NONE
"""

from gllm_core.schema import Chunk
from gllm_retrieval.reranker.reranker import BaseReranker


class NoOpReranker(BaseReranker):
    """No-op reranker implementation."""

    async def rerank(self, chunks: list[Chunk], query: str | None = None) -> list[Chunk]:  # noqa: ARG002
        """No-op reranker that returns the input chunks as is.

        Args:
            chunks (list[Chunk]): The list of chunks to be reranked.
            query (str | None, optional): The query to be used for reranking. Defaults to None.

        Returns:
            list[Chunk]: The input chunks as is.
        """
        return chunks
