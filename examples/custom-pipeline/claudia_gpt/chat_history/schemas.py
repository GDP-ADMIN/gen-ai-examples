"""Chat History models.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

import json
from datetime import datetime
from enum import Enum
from typing import Any

from gllm_inference.schema import PromptRole
from pydantic import BaseModel, ConfigDict, field_validator

from claudia_gpt.constant.agent_type import AgentType


class MessageRole(str, Enum):
    """Enum for Message Type."""

    USER = PromptRole.USER.value
    AI = PromptRole.ASSISTANT.value


class Message(BaseModel):
    """Message model.

    Represents a message in a conversation.

    Attributes:
        id (str | None): The unique identifier of the message.
        conversation_id (str): The identifier of the conversation this message belongs to.
        role (MessageRole): The role of the sender of the message (USER or AI).
        content (str): The text content of the message.
        deanonymized_content (str | None): The deanonymized content of the message.
        created_date (datetime): The timestamp when the message was created.
        is_active (bool): Indicates if the message is active.
        parent_id (str | None): The identifier of the parent message, if any.
        source (str | None): The source of the message.
        feedback (str | None): The feedback of the message.
        agent_type (AgentType): The type of the agent that generated the message.
        metadata_ (dict[str, Any] | None): The metadata of the message.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str | None = None
    conversation_id: str
    role: MessageRole
    content: str
    deanonymized_content: str | None = None
    created_date: datetime
    is_active: bool
    parent_id: str | None = None
    source: str | None = None
    feedback: str | None = None
    agent_type: AgentType
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
            return json.loads(value)
        return value


class Conversation(BaseModel):
    """Conversation model.

    Attributes:
        id (str): The conversation ID.
        user_id (str): The user ID.
        title (str | None): The conversation title.
        created_date (datetime): The creation date.
        updated_date (datetime): The last update date.
        is_active (bool): Whether the conversation is active.
        tenant (str | None): The tenant ID.
        is_anonymized (bool): Whether the conversation is anonymized.
        chatbot_id (str): The chatbot ID.
        deanonymized_mapping (dict[str, str]): Mapping of anonymized to original values.
        first_matching_message_id (str | None): First message ID that matches search query.
        first_matching_message (str | None): First message that matches search query.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    title: str | None
    created_date: datetime
    updated_date: datetime
    is_active: bool
    tenant: str | None = None
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
    created_time: datetime
    last_updated_time: datetime
    expired_time: datetime | None = None  # None means never expires
    is_active: bool = True
