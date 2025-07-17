"""Contains the base class for rerankers.

It is adjusted from BaseReranker from Gen AI SDK to make the type hints more specific.

Authors:
    Muhammad Afif Al Hawari (muhammad.a.a.hawari@gdplabs.id)

References:
    [1] https://docs.glair.ai/generative-internal/modules/retrieval/reranker
"""

from abc import ABC, abstractmethod

from langchain_core.documents import Document


class BaseReranker(ABC):
    """Base class for rerankers."""

    @abstractmethod
    def get_reranked_documents(self, documents: list[Document], query: str) -> list[Document]:
        """Reranks a set of documents based on certain criteria."""
        raise NotImplementedError
