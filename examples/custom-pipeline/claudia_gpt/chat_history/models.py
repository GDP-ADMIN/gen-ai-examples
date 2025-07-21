"""DB Model Class for database table.

These classes are used to define the database schema for the application.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)
"""

from datetime import datetime, timezone

import sqlalchemy as sa
from gllm_datastore.sql_data_store.adapter.sqlalchemy_adapter import SQLAlchemyAdapter

from claudia_gpt.chat_history.schemas import DocumentStatus, MessageRole


class ConversationModel(SQLAlchemyAdapter.base):
    """Base Database Model Class for Conversation Table."""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "conversation"
    id = sa.Column(sa.String(36), primary_key=True)
    user_id = sa.Column(sa.String(100))
    title = sa.Column(sa.String(100))
    created_time = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_time = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = sa.Column(sa.Boolean, default=True)
    is_anonymized = sa.Column(sa.Boolean, default=True)
    project_id = sa.Column(sa.String(36))


class MessageModel(SQLAlchemyAdapter.base):
    """Base Database Model Class for Message Table."""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "message"
    id = sa.Column(sa.String(36), primary_key=True)
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversation.id"))
    role = sa.Column(sa.Enum(MessageRole))
    content = sa.Column(sa.TEXT)
    created_time = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    is_active = sa.Column(sa.Boolean, default=True)
    feedback = sa.Column(sa.TEXT, nullable=True)
    parent_id = sa.Column(sa.String(36), nullable=True)
    source = sa.Column(sa.String(20), nullable=True)
    metadata_ = sa.Column(sa.TEXT, nullable=True)


class ConversationDocumentModel(SQLAlchemyAdapter.base):
    """Base Database Model Class for DocumentStatus Table."""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "conversation_document"
    id = sa.Column(sa.String(101), primary_key=True)
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversation.id"))
    status = sa.Column(sa.Enum(DocumentStatus))
    number_of_chunks = sa.Column(sa.Integer(), nullable=False, default=0)
    message = sa.Column(sa.TEXT, nullable=True)
    object_key = sa.Column(sa.TEXT, nullable=True)


class SharedConversationModel(SQLAlchemyAdapter.base):
    """Base Database Model Class for SharedConversation Table."""

    __table_args__ = {"extend_existing": True}
    __tablename__ = "shared_conversation"
    id = sa.Column(sa.String(36), primary_key=True)
    user_id = sa.Column(sa.String(100))
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversation.id"))
    created_time = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    last_updated_time = sa.Column(sa.DateTime, default=lambda: datetime.now(timezone.utc))
    expired_time = sa.Column(sa.DateTime, nullable=True)
    is_active = sa.Column(sa.Boolean, default=True)
