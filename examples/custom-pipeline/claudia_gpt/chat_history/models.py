"""DB Model Class for database table.

These classes are used to define the database schemas for the application.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
"""

import uuid
from datetime import datetime

import sqlalchemy as sa

from claudia_gpt.chat_history.schemas import DocumentStatus, MessageRole
from claudia_gpt.constant.agent_type import AgentType
from claudia_gpt.db.adapter import DatabaseAdapter


class ConversationModel(DatabaseAdapter.base):
    """Base Database Model Class for Conversation Table.

    Attributes:
        id (sa.Column): The unique identifier for the conversation, generated as a UUID.
        user_id (sa.Column): The ID of the user who created the conversation.
        title (sa.Column): The title of the conversation.
        tenant (sa.Column): The tenant associated with the conversation.
        created_date (sa.Column): The timestamp when the conversation was created, in milliseconds.
        updated_date (sa.Column): The timestamp when the conversation was updated, in milliseconds.
        is_active (sa.Column): A boolean indicating whether the conversation is active.
        is_anonymized (sa.Column): A boolean indicating whether the conversation is anonymized.
        project_id (sa.Column): The ID of the project associated with the conversation.
    """

    __tablename__ = "conversations"
    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = sa.Column(sa.String(50))
    title = sa.Column(sa.String(100))
    tenant = sa.Column(sa.String(255), nullable=True)
    created_date = sa.Column(sa.BigInteger, default=lambda: int(datetime.now().timestamp() * 1000.0))
    updated_date = sa.Column(sa.BigInteger, default=lambda: int(datetime.now().timestamp() * 1000.0))
    is_active = sa.Column(sa.Boolean, default=True)
    is_anonymized = sa.Column(sa.Boolean, default=True)
    project_id = sa.Column(sa.String(36))


class MessageModel(DatabaseAdapter.base):
    """Base Database Model Class for Message Table.

    Attributes:
        id (sa.Column): The unique identifier for the message, generated as a UUID.
        conversation_id (sa.Column): The ID of the conversation this message belongs to.
        role (sa.Column): The role of the sender of the message, represented as an enumeration.
        content (sa.Column): The encrypted or encoded message.
        created_date (sa.Column): The timestamp when the message was created, in milliseconds.
        is_active (sa.Column): A boolean indicating whether the message is active.
        feedback (sa.Column): A JSON field for storing feedback associated with the message.
        agent_type (sa.Column): The type of agent that sent the message.
        parent_id (sa.Column): The ID of the parent message, if any.
        source (sa.Column): The source of the message.
        metadata_ (sa.Column): The metadata of the message.
    """

    __tablename__ = "messages"
    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversations.id"))
    role = sa.Column(sa.Enum(MessageRole))
    content = sa.Column(sa.BLOB, nullable=False)
    created_date = sa.Column(sa.BigInteger, default=lambda: int(datetime.now().timestamp() * 1000.0))
    is_active = sa.Column(sa.Boolean, default=True)
    feedback = sa.Column(sa.TEXT, nullable=True)
    agent_type = sa.Column(sa.String(100), nullable=False)
    parent_id = sa.Column(sa.String(36), nullable=True)
    source = sa.Column(sa.String(20), nullable=True)
    metadata_ = sa.Column(sa.TEXT, nullable=True)

    __mapper_args__ = {"polymorphic_on": "agent_type", "polymorphic_identity": AgentType.DATA_ANALYST.value}


class ConversationDocumentModel(DatabaseAdapter.base):
    """Base Database Model Class for DocumentStatus Table.

    Attributes:
        __tablename__ (str): The name of the table in the database.
        id (sa.Column): The unique identifier for the document.
        conversation_id (sa.Column): The ID of the conversation this document belongs to.
        status (sa.Column): The status of the document.
        number_of_chunks (sa.Column): The number of chunks in the document.
        message (sa.Column): The message of the document.
        object_key (sa.Column): The object key of the document.
    """

    __tablename__ = "conversation_documents"
    id = sa.Column(sa.String(101), primary_key=True)
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversations.id"))
    status = sa.Column(sa.Enum(DocumentStatus))
    number_of_chunks = sa.Column(sa.Integer(), nullable=False, default=0)
    message = sa.Column(sa.TEXT, nullable=True)
    object_key = sa.Column(sa.TEXT, nullable=True)


class MessageContextModel(MessageModel):
    """Database Model Class for Message Context Table.

    Attributes:
        id (sa.Column): The unique identifier for the message, generated as a UUID.
        context (sa.Column): The context of the message.
    """

    __tablename__ = "message_contexts"

    id = sa.Column(sa.String(36), sa.ForeignKey("messages.id"), primary_key=True)
    context = sa.Column(sa.TEXT, nullable=True)


class HelpCenterCatapaMessageModel(MessageContextModel):
    """Database Model Class for Help Center Catapa Messages Table."""

    __mapper_args__ = {"polymorphic_identity": AgentType.HELP_CENTER_CATAPA.value}


class RegulationMessageModel(MessageContextModel):
    """Database Model Class for Regulation Messages Table."""

    __mapper_args__ = {"polymorphic_identity": AgentType.REGULATION.value}


class MCPMessageModel(MessageContextModel):
    """Database Model Class for MCP Messages Table."""

    __mapper_args__ = {"polymorphic_identity": AgentType.MCP.value}


class EssMessageModel(MessageModel):
    """Database Model Class for ESS Messages.

    This class shares the same table as data analyst messages.
    """

    __mapper_args__ = {"polymorphic_identity": AgentType.ESS_ASSISTANT.value}


class NLWebMessageModel(MessageModel):
    """Database Model Class for NLWeb Messages.

    This class shares the same table as data analyst messages.
    """

    __mapper_args__ = {"polymorphic_identity": AgentType.NLWEB.value}


class SharedConversationModel(DatabaseAdapter.base):
    """Base Database Model Class for SharedConversation Table."""

    __tablename__ = "shared_conversation"
    id = sa.Column(sa.String(36), primary_key=True)
    user_id = sa.Column(sa.String(100))
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversation.id"))
    created_date = sa.Column(sa.DateTime, default=lambda: int(datetime.now().timestamp() * 1000.0))
    last_updated_time = sa.Column(sa.DateTime, default=lambda: int(datetime.now().timestamp() * 1000.0))
    expired_time = sa.Column(sa.DateTime, nullable=True)
    is_active = sa.Column(sa.Boolean, default=True)
