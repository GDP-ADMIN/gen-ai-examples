"""Chat history manager component for MCP Pipeline.

Authors:
    Samuel Lusandi (samuel.lusandi@gdplabs.id)
"""

import datetime
import uuid

from typing import Any
from pydantic import BaseModel

from gllm_core.event import EventEmitter as EventEmitter
from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore


class Message(BaseModel):
    """A message object containing all necessary information."""
    id: str
    conversation_id: str
    role: str
    content: str
    parent_id: str
    created_time: datetime.datetime
    is_active: bool
    feedback: str
    source: str
    metadata_: str


class McpChatHistoryManager(Component):
    """Chat history manager component."""

    def __init__(
        self,
        data_store: SQLAlchemySQLDataStore,
    ):
        """Initialize the chat history manager."""
        self.data_store = data_store

    async def _run(self, **kwargs: str) -> Any:
        """Run the chat history manager component.

        Args:
            kwargs (Any): The keyword arguments, which may contain the operation.

        Returns:
            Any: The result of the operation.
        """
        if not self.data_store:
            return None

        operation = kwargs.get("operation")

        if operation == "read":
            return await self.read(kwargs)

        if operation == "write":
            return await self.write(kwargs)

    async def read(self, kwargs: dict[str, Any]) -> Any:
        """Read the chat history.

        Args:
            kwargs (dict[str, Any]): The keyword arguments.

        Returns:
            Any: The chat history.
        """
        return None

    async def write(self, kwargs: dict[str, Any]) -> Any:
        """Write the chat history.

        Args:
            kwargs (dict[str, Any]): The keyword arguments.

        Returns:
            Any: The chat history.
        """
        user_message = Message(
            id=kwargs.get("user_message_id") or str(uuid.uuid4()),
            conversation_id=kwargs.get("conversation_id"),
            role="user",
            content=kwargs.get("query"),
            parent_id=kwargs.get("parent_id") or kwargs.get("conversation_id"),
            created_time=datetime.datetime.now(datetime.UTC),
            is_active=kwargs.get("is_active", True),
            feedback=None,
            source="user",
            metadata_="{}",
        )
        assistant_message = Message(
            id=kwargs.get("assistant_message_id") or str(uuid.uuid4()),
            conversation_id=kwargs.get("conversation_id"),
            role="assistant",
            content=kwargs.get("response"),
            parent_id=user_message.id,
            created_time=datetime.datetime.now(datetime.UTC),
            is_active=kwargs.get("is_active", True),
            feedback=None,
            source=kwargs.get("source"),
            metadata_="{}",
        )
        self.data_store.create([user_message, assistant_message])
        return ""
