"""Custom data store for the gen_ai_hello_world application.

This is a mock data store for the gen_ai_hello_world application.
In production, you should use other implementation of DataStore.
"""

from typing import Any

from gllm_core.schema import Chunk
from gllm_retrieval.constants import DEFAULT_TOP_K
from gllm_retrieval.retriever.data_store.data_store import BaseDataStore


class CustomDataStore(BaseDataStore):
    """Custom data store for the gen_ai_hello_world application."""

    async def query(
        self,
        query: str,
        top_k: int = DEFAULT_TOP_K,
        retrieval_params: dict[str, Any] | None = None,
    ) -> list[Chunk]:
        """Query the data store."""
        # Return mock data
        mock_chunks = [
            Chunk(id="1", content="Mock document 1", metadata={"source": "mock_source_1"}),
            Chunk(id="2", content="Mock document 2", metadata={"source": "mock_source_2"}),
            Chunk(id="3", content="Mock document 3", metadata={"source": "mock_source_3"}),
        ]
        return mock_chunks[:top_k]

    async def query_by_id(self, id_: str | list[str]) -> list[Chunk]:
        """Query the data store by ID."""
        raise NotImplementedError
