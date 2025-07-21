"""Chat History models.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

import json
from datetime import datetime
from enum import Enum, StrEnum
from typing import Any

from gllm_inference.schema import PromptRole
from pydantic import BaseModel, ConfigDict, field_validator


class MessageRole(StrEnum):
    """Enum for Message Type."""

    user = PromptRole.USER.value
    assistant = PromptRole.ASSISTANT.value


class Message(BaseModel):
    """Message model."""

    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    conversation_id: str
    role: MessageRole
    content: str
    deanonymized_content: str | None = None
    created_time: datetime
    is_active: bool
    parent_id: str | None = None
    source: str | None = None
    feedback: str | None = None
    metadata_: dict[str, Any] | None = None

    @field_validator("metadata_", mode="before")
    def parse_metadata(cls, value: str | dict[str, Any]) -> dict[str, Any]:  # noqa: B902
        """Parse the metadata_ field if it's a string, converting it to a JSON object.

        Args:
            value (str | dict[str, Any]): Value to be parsed.

        Returns:
            dict[str, Any]: Parsed value.
        """
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(f"Failed to parse metadata: {value}", value, 0) from e
        return value


class Conversation(BaseModel):
    """Conversation model.

    Attributes:
        id (str): The conversation ID.
        user_id (str): The user ID.
        title (str | None): The conversation title.
        created_time (datetime): The creation time.
        updated_time (datetime): The last update time.
        is_active (bool): Whether the conversation is active.
        chatbot_id (str): The chatbot ID.
        is_anonymized (bool): Whether the conversation is anonymized.
        deanonymized_mapping (dict[str, str]): Mapping of anonymized to original values.
        first_matching_message_id (str | None): First message ID that matches search query.
        first_matching_message (str | None): First message that matches search query.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str | None
    created_time: datetime
    updated_time: datetime
    is_active: bool
    is_anonymized: bool
    chatbot_id: str
    deanonymized_mapping: dict[str, str] = {}
    first_matching_message_id: str | None = None
    first_matching_message: str | None = None

    @classmethod
    def from_model(cls, conversation_model: "ConversationModel") -> "Conversation":  # noqa: F821
        """Convert ConversationModel to Conversation.

        Args:
            conversation_model (ConversationModel): Database model instance

        Returns:
            Conversation: Pydantic model instance
        """
        data = conversation_model.__dict__
        data["chatbot_id"] = data.pop("project_id")
        return cls.model_validate(data)

    @field_validator("title", mode="before")
    def _ensure_title_is_str(cls, value: str | None) -> str:
        """Ensure the title is a string.

        Args:
            value (str | None): The value to be ensured.

        Returns:
            str: The ensured value.
        """
        return value or ""

    def redact_user_id(self) -> None:
        """Redact sensitive user_id field."""
        self.user_id = ""


class DocumentStatus(Enum):
    """Enum for ConversationDocument Status."""

    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"


class ConversationDocument(BaseModel):
    """ConversationDocument model."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    status: DocumentStatus
    number_of_chunks: int = 0
    message: str | None = None
    object_key: str | None = None


class ObjectStorageType(Enum):
    """Enumeration for object storage types."""

    MINIO = "minio"

    def __str__(self) -> str:
        """Return the string representation of the object storage type."""
        return self.value


class MessageReference(BaseModel):
    """Message Refererence model."""

    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    title: str | None = None
    name: str | None = None
    type: str | None = None
    content: str | None = None
    url: str | None = None


class SharedConversation(BaseModel):
    """shared conversation model."""

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    conversation_id: str
    title: str | None = None
    created_time: datetime
    last_updated_time: datetime
    expired_time: datetime | None = None  # None means never expires
    first_matching_word: str | None = None
    is_active: bool = True
