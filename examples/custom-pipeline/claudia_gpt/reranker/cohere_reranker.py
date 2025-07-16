"""Contains the CohereReranker class.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)

References:
    NONE
"""

import cohere
from cohere.core import ApiError
from gllm_core.schema import Chunk
from gllm_retrieval.reranker.reranker import BaseReranker

from claudia_gpt.config.schemas.reranker_schema import CohereRerankerConfig

# from claudia_gpt.utils.logger import logger


class CohereReranker(BaseReranker):
    """Reranks a list of documents using a Cohere reranker.

    Attributes:
        config (CohereRerankerConfig): The configuration for the Cohere reranker.
        client (cohere.Client): The Cohere client for reranking documents.
    """

    def __init__(self, config: CohereRerankerConfig) -> None:
        """Initializes a new instance of the CohereReranker class.

        Args:
            config (CohereRerankerConfig): The configuration for the Cohere reranker.
        """
        self.config = config
        if not self.config.api_key:
            raise ValueError("API key for CohereReranker is missing.")
        self.client = cohere.Client(self.config.api_key)

    async def rerank(self, chunks: list[Chunk], query: str | None = None) -> list[Chunk]:
        """Rerank the list of chunks.

        Args:
            chunks (list[Chunk]): The list of chunks to be reranked.
            query (str | None, optional): The query to be used for reranking. Defaults to None.

        Returns:
            list[Chunk]: A list of reranked chunks.

        Raises:
            ApiError: If an error occurs while reranking documents.
        """
        if len(chunks) <= 1:
            return chunks

        try:
            chunk_contents = [chunk.content for chunk in chunks]
            response = self.client.rerank(
                model=self.config.model,
                query=query,
                documents=chunk_contents,
            )
            reranked_indexes = [item.index for item in response.results]
            reranked_chunks = [chunks[i] for i in reranked_indexes]
            return reranked_chunks
        except ApiError as error:
            # logger.error(f"An error occurred while reranking documents: {error}")
            return chunks
