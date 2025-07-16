"""Response models for the API.

These models are used to define the response structure for the API.
The fields in these models can be different from the source where the data is fetched.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)

References:
    None
"""

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel

from claudia_gpt.api.model.constant import SearchType
from claudia_gpt.chat_history.schemas import Conversation, Message, MessageRole


class MessageItem(BaseModel):
    """Model for a message item.

    Attributes:
        id (Optional[str]): The unique identifier of the message.
        role (MessageRole): The role of the message sender (e.g., user, system).
        content (str): The content of the message.
        source (Optional[str]): The source of the message, if applicable.
        parent_id (Optional[str]): The ID of the parent message, if applicable.
    """

    id: Optional[str] = None
    role: MessageRole
    content: str
    source: Optional[str] = None
    parent_id: Optional[str] = None


class HealthcheckResponse(BaseModel):
    """Response model for health check API.

    Attributes:
        message (str): The health check status message.
    """

    message: str


class UpdateConfigResponse(BaseModel):
    """Response model for updating the configuration.

    Attributes:
        message (str): The status message for the configuration update.
    """

    message: str


class CreateConversationResponse(BaseModel):
    """Response model for creating a conversation.

    Attributes:
        conversation (Conversation): The created conversation details.
    """

    conversation: Conversation


class GetConversationsResponse(BaseModel):
    """Response model for getting all conversations.

    Attributes:
        conversations (list[Conversation]): List of conversations.
        cursor (Optional[str]): A cursor for pagination, if applicable.
        conversations_count (int): The total count of conversations.
    """

    conversations: list[Conversation]
    cursor: str | None = None
    conversations_count: int


class GetConversationMessagesResponse(BaseModel):
    """Response model for getting conversation messages.

    Attributes:
        conversation (Conversation): The conversation details.
        messages (list[Message]): List of messages in the conversation.
        attachments (list[dict[str, str | int]]): List of attachments related to the messages.
    """

    conversation: Conversation
    messages: list[Message]
    attachments: list[dict[str, str | int]]


class GetDeanonymizedMessageResponse(BaseModel):
    """Response model for getting a deanonymized message.

    Attributes:
        message (Message): The deanonymized message.
    """

    message: Message


class ChatbotModelItem(BaseModel):
    """Model for a chatbot model item.

    Attributes:
        name (str): The name of the chatbot model.
        icon (str): The icon representing the chatbot model.
        supported_attachments (dict[str, list[str]]): Supported attachment types and formats.
        max_file_size (int | None): The maximum file size supported by the chatbot model.
    """

    name: str
    display_name: str
    description: str
    icon: str
    supported_attachments: dict[str, list[str]]
    max_file_size: int | None = None


class ChatbotItem(BaseModel):
    """Model for a chatbot item.

    Attributes:
        id (str): The unique identifier for the chatbot.
        display_name (str): The display name of the chatbot.
        description (str): A brief description of the chatbot.
        models (list[ChatbotModelItem]): List of models supported by the chatbot.
        agents (list[dict[str, Any]]): List of agents supported by the chatbot.
        support_pii_anonymization (bool): Whether the chatbot supports anonymizing
            personally identifiable information (PII).
        default_pii_anonymization (bool): Whether the chatbot anonymizes PII by default.
        search_types (list[SearchType]): List of supported search types for the chatbot.
        recommended_questions (list[str]): List of recommended questions for the chatbot.
    """

    id: str
    display_name: str
    description: str
    models: list[ChatbotModelItem]
    agents: list[dict[str, Any]]
    support_pii_anonymization: bool
    default_pii_anonymization: bool
    search_types: list[SearchType]
    discovery_providers: dict[str, str]
    recommended_questions: list[str]


class GetUserChatbotsResponse(BaseModel):
    """Response model for getting user chatbots.

    Attributes:
        chatbots (list[ChatbotItem]): List of chatbots available to the user.
    """

    chatbots: list[ChatbotItem]


class KnowledgeBaseItem(BaseModel):
    """Model for a knowledge base item.

    Attributes:
        id (str): The unique identifier for the knowledge base item.
        type (str): The type of knowledge base (e.g., document, FAQ, etc.).
        name (str): The name of the knowledge base item.
        description (str): A brief description of the knowledge base item.
    """

    id: str
    type: str
    name: str
    description: str


class GetUserKnowledgeBasesResponse(BaseModel):
    """Response model for getting user knowledge bases.

    Attributes:
        knowledge_bases (list[KnowledgeBaseItem]): List of knowledge bases available to the user.
    """

    knowledge_bases: list[KnowledgeBaseItem]


class SharedConversationResponse(BaseModel):
    """Response model for sharing a conversation.

    Attributes:
        shared_conversation_id (str): The unique identifier for the shared conversation.
        last_updated_time (datetime): The last time the shared conversation was updated.
        expired_time (datetime | None): When the shared conversation access id expires. Defaults to None (no expiry).
    """

    shared_conversation_id: str
    last_updated_time: datetime
    expired_time: datetime | None = None


class GetSharedConversationResponse(BaseModel):
    """Response model for getting a shared conversation.

    Attributes:
        messages (list[Message]): List of messages in the shared conversation.
        conversation (Conversation): The conversation details.
        user_id (str): ID of the user who created the shared conversation.
        last_updated_time (datetime): The last time the shared conversation was updated.
        expired_time (datetime | None): When the shared conversation access id expires.
        attachments (list[dict[str, Any]]): List of attachments in the conversation.
        chatbot (dict[str, Any]): The chatbot associated with the conversation.
    """

    messages: list[Message]
    conversation: Conversation
    user_id: str
    last_updated_time: datetime
    expired_time: datetime | None = None
    attachments: list[dict[str, Any]] = []
    chatbot: dict[str, Any]
