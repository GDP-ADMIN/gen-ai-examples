"""Chat History module.

This module contains the class for handling chat history.
A "conversation" contains a list of messages. Each message has a type (user or AI message), and content.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

import copy
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import sqlalchemy
from glchat_plugin.storage.base_chat_history_storage import BaseChatHistoryStorage
from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from gllm_privacy.pii_detector import TextAnalyzer, TextAnonymizer
from gllm_privacy.pii_detector.utils.deanonymizer_mapping import DeanonymizerMapping
from sqlalchemy import and_, desc, func, or_, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Query
from sqlalchemy.orm.session import Session

from claudia_gpt.anonymizer.schemas import AnonymizerMapping
from claudia_gpt.chat_history.models import (
    ConversationDocumentModel,
    ConversationModel,
    MessageModel,
    SharedConversationModel,
)
from claudia_gpt.chat_history.schemas import (
    Conversation,
    ConversationDocument,
    DocumentStatus,
    Message,
    MessageRole,
    SharedConversation,
)
from claudia_gpt.config.constant import (
    SharedConversationConstants,
)
from claudia_gpt.utils.logger import logger

# Note: SQL apostrophes need to be doubled within string literals
FEEDBACK_REASON_CATEGORIES = [
    "Don''t Know",
    "Confused",
    "Same as before",
    "Not sure",
    "Don''t feel happy",
    "Don''t like the suggestion",
    "Not factually correct",
    "Hallucinated answer",
    "Didn''t fully follow instructions",
]


class ChatHistoryStorage(BaseChatHistoryStorage):
    """Class for handling chat history."""

    def __init__(
        self,
        data_store: SQLAlchemySQLDataStore,
        text_analyzer: TextAnalyzer,
    ):
        """Initialize ChatHistory class.

        Args:
            data_store (SQLAlchemySQLDataStore): Chat history data store.
            text_analyzer (TextAnalyzer): Text analyzer.
        """
        self.db = data_store.db
        self.text_analyzer = text_analyzer

    def get_conversations(
        self,
        user_id: str,
        query: str = "",
        chatbot_ids: list[str] | None = None,
        cursor: str | None = None,
        limit: int | None = None,
        **kwargs: Any,
    ) -> tuple[int, list[Conversation]]:
        """Get list of conversations for a user.

        Args:
            user_id (str): User ID.
            query (str): Search query for conversation title or message content. Default is an empty string.
            chatbot_ids (list[str] | None): List of Chatbot IDs. Defaults to None.
            cursor (str | None): The updated_time of the last conversation fetched in ISO 8601 string format
                            (for cursor-based pagination). Defaults to None.
            limit (int | None): Number of conversations to return per request. Defaults to None.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            tuple[int, list[Conversation]]: A tuple containing:
                - The total number of conversations matching the query
                - List of paginated conversations.

        Raises:
            ValueError: If cursor format is invalid or if database operation fails.
        """
        try:
            with self.db() as session:
                base_query = self._get_filtered_query(session, user_id, query, chatbot_ids, cursor)

                # Get total count
                total_count: int = self._get_distinct_conversations_count(session, base_query)

                # Get paginated conversations
                conversation_list = self._get_paginated_conversations(base_query, limit)

                # Add matching messages if query exists
                if query:
                    self._add_matching_messages(session, conversation_list, query)

                return total_count, conversation_list

        except SQLAlchemyError as e:
            logger.error(f"Database error while fetching conversations: {e}")
            raise ValueError("Failed to fetch conversations") from e

    def _get_filtered_query(
        self, session: Session, user_id: str, query: str, chatbot_ids: list[str] | None, cursor: str | None
    ) -> Query[ConversationModel]:
        """Build and return filtered conversation query.

        Args:
            session (Session): SQLAlchemy session.
            user_id (str): User ID.
            query (str): Search query for conversation title or message content.
            chatbot_ids (list[str] | None): List of Chatbot IDs. Defaults to None.
            cursor (str | None): The updated_time of the last conversation fetched in ISO 8601 string format
                            (for cursor-based pagination). Defaults to None.

        Returns:
            Query[ConversationModel]: The filtered query, filtered by user_id, is_active, chatbot_ids, and query.
        """
        base_query = session.query(ConversationModel).filter(
            ConversationModel.user_id == user_id,
            ConversationModel.is_active.is_(True),
        )

        if chatbot_ids:
            base_query = base_query.filter(ConversationModel.project_id.in_(chatbot_ids))

        if query:
            sanitized_query = text(query)
            base_query = base_query.outerjoin(
                MessageModel, ConversationModel.id == MessageModel.conversation_id
            ).filter(
                or_(
                    ConversationModel.title.ilike(f"%{sanitized_query}%"),
                    and_(
                        MessageModel.content.ilike(f"%{sanitized_query}%"),
                        MessageModel.is_active.is_(True),
                    ),
                )
            )

        if cursor:
            try:
                cursor_datetime = datetime.fromisoformat(cursor)
                base_query = base_query.filter(ConversationModel.updated_time < cursor_datetime)
            except ValueError as err:
                raise ValueError("Invalid cursor format.") from err

        distinct_ids_subquery = (
            session.query(ConversationModel.id)
            .filter(ConversationModel.id.in_(base_query.with_entities(ConversationModel.id)))
            .distinct()
        )

        base_query = (
            session.query(ConversationModel)
            .filter(ConversationModel.id.in_(distinct_ids_subquery))
            .order_by(desc(ConversationModel.updated_time))
        )

        return base_query

    def _get_distinct_conversations_count(self, session: Session, query: Query[ConversationModel]) -> int:
        """Get a total count of distinct conversations with messages matching the criteria.

        Args:
            session (Session): SQLAlchemy session.
            query (Query[ConversationModel]): Query result, filtered by user_id, chatbot_id, query, and is_active.

        Returns:
            int: The total count of conversations matching the criteria.
        """
        # Create a subquery and alias it to isolate the results for further processing
        subquery = query.subquery()
        alias_subquery = sqlalchemy.orm.aliased(subquery)

        # Construct and execute a count query to get the total distinct conversation IDs
        count_query = session.query(func.count(func.distinct(alias_subquery.c.id))).select_from(alias_subquery)
        total_count = count_query.scalar()

        return total_count

    def _get_paginated_conversations(self, query: Query[ConversationModel], limit: int | None) -> list[Conversation]:
        """Get paginated conversations.

        Args:
            query (Query[ConversationModel]): Base query result.
            limit (int | None): Number of conversations to return per request. Defaults to None.

        Returns:
            list[Conversation]: List of paginated conversations.
        """
        if limit:
            query = query.limit(limit)

        conversation_models = query.all()
        return [Conversation.from_model(obj) for obj in conversation_models]

    def _add_matching_messages(self, session: Session, conversations: list[Conversation], query: str) -> None:
        """Add first matching message to each conversation for the search query.

        Args:
            session (Session): SQLAlchemy session.
            conversations (list[Conversation]): List of conversations.
            query (str): Search query for message content.
        """
        sanitized_query = text(query)
        first_messages = (
            session.query(
                MessageModel.conversation_id,
                MessageModel.id.label("message_id"),
                func.first_value(MessageModel.content)
                .over(partition_by=MessageModel.conversation_id, order_by=MessageModel.created_time)
                .label("content"),
            )
            .filter(
                MessageModel.conversation_id.in_([conv.id for conv in conversations]),
                MessageModel.is_active.is_(True),
                MessageModel.content.ilike(f"%{sanitized_query}%"),
            )
            .distinct(MessageModel.conversation_id)
            .all()
        )

        conv_message_map = {msg.conversation_id: (msg.content, msg.message_id) for msg in first_messages}
        for conv in conversations:
            conv.first_matching_message, conv.first_matching_message_id = conv_message_map.get(conv.id, (None, None))

    def get_conversation(self, user_id: str, conversation_id: str, **kwargs: Any) -> Conversation | None:
        """Get conversation by ID.

        Args:
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Conversation | None: Conversation object if found, otherwise None.
        """
        with self.db() as session:
            conversation = self._get_conversation(session, user_id, conversation_id)
            return Conversation.from_model(conversation) if conversation else None

    def create_conversation(
        self, user_id: str, conversation_title: str | None, chatbot_id: str, **kwargs: Any
    ) -> Conversation:
        """Create new conversation.

        Args:
            user_id (str): User ID.
            conversation_title (str | None): Conversation title, default to None.
            chatbot_id (str): Chatbot ID
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Conversation: Newly created Conversation object.
        """
        with self.db() as session:
            try:
                new_conversation = ConversationModel(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    title=conversation_title,
                    project_id=chatbot_id,
                )
                session.add(new_conversation)
                session.commit()
                session.refresh(new_conversation)

                conversation = Conversation.from_model(new_conversation)
                return conversation
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def rename_conversation(self, user_id: str, conversation_id: str, new_title: str, **kwargs: Any) -> Conversation:
        """Rename a conversation.

        Args:
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            new_title (str): Conversation title.
            kwargs (Any): Additional keyword arguments.

        Returns:
            Conversation: Updated Conversation object.
        """
        with self.db() as session:
            try:
                conversation = self._get_conversation(session, user_id, conversation_id)
                self._validate_conversation_exists(conversation_id, conversation)

                conversation.title = new_title
                session.commit()
                session.refresh(conversation)

                updated_conversation = Conversation.from_model(conversation)
                return updated_conversation
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def add_user_message(  # noqa: PLR0913
        self,
        message: str,
        user_id: str,
        conversation_id: str,
        parent_id: str | None = None,
        source: str | None = None,
        conversation: Conversation | None = None,
        metadata_: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Message:
        """Add user message to a conversation.

        Args:
            message (str): Message content.
            user_id (str): User ID.
            conversation_id (str): Existing conversation ID.
            parent_id (str | None): Parent message ID. Defaults to None.
            source (str | None): Source of the message. Defaults to None.
            conversation (Conversation | None): Conversation object if any. Defaults to None.
            metadata_ (dict[str, Any] | None): Additional metadata for the message. Defaults to None.
            kwargs (Any): Additional keyword arguments.

        Returns:
            Message: Newly created Message object.
        """
        return self.add_message(
            message_role=MessageRole.user,
            message=message,
            user_id=user_id,
            conversation_id=conversation_id,
            parent_id=parent_id,
            source=source,
            conversation=conversation,
            metadata_=metadata_,
            **kwargs,
        )

    def add_ai_message(  # noqa: PLR0913
        self,
        message: str,
        user_id: str,
        conversation_id: str,
        parent_id: str | None = None,
        source: str | None = None,
        conversation: Conversation | None = None,
        metadata_: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Message:
        """Add AI message to a conversation.

        Args:
            message (str): Message content.
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            parent_id (str | None): Parent message ID. Defaults to None.
            source (str | None): Source of the message. Defaults to None.
            conversation (Conversation | None): Conversation object if any. Defaults to None.
            metadata_ (dict[str, Any] | None): Additional metadata for the message. Defaults to None.
            kwargs (Any): Additional keyword arguments.

        Returns:
            Message: Newly created Message object.
        """
        return self.add_message(
            message_role=MessageRole.assistant,
            message=message,
            user_id=user_id,
            conversation_id=conversation_id,
            parent_id=parent_id,
            source=source,
            conversation=conversation,
            metadata_=metadata_,
            **kwargs,
        )

    def add_message(  # noqa: PLR0913
        self,
        message_role: MessageRole,
        message: str,
        user_id: str,
        conversation_id: str,
        parent_id: str,
        source: str,
        conversation: Conversation | None = None,
        metadata_: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> Message:
        """Add message to a conversation.

        Args:
            message_role (MessageType): Message type.
            message (str): Message content.
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            parent_id (str): Parent message ID.
            source (str): Source of the message.
            conversation (Conversation | None): Conversation object if any. Defaults to None.
            metadata_ (dict[str, Any] | None): Additional metadata for the message. Defaults to None.
            kwargs (Any): Additional keyword arguments.

        Returns:
            Message: Newly created Message object.
        """
        with self.db() as session:
            try:
                conversation = conversation or self._get_conversation(session, user_id, conversation_id)
                self._validate_conversation_exists(conversation_id, conversation)

                message_id = kwargs.get("id", str(uuid.uuid4()))
                logger.info(f"add_message: Creating message with id={message_id}")

                metadata_text = self._serialize_metadata(metadata_)

                logger.debug(f"Add metadata in conversation {conversation_id} : {metadata_}")
                new_message = MessageModel(
                    id=message_id,
                    conversation_id=conversation_id,
                    role=message_role,
                    content=message,
                    parent_id=parent_id,
                    source=source,
                    metadata_=metadata_text,
                )
                session.add(new_message)
                conversation.updated_time = datetime.now(timezone.utc)
                session.commit()

                message_obj = Message.model_validate(new_message)
                return message_obj
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def save_message(
        self,
        user_id: str,
        conversation_id: str,
        message_list: list[Any],
        attachments: dict[str, Any] | None = None,
    ) -> list[Message]:
        """Save message.

        Args:
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            message_list (list[Message]): List of messages.
            attachments (dict[str, Any] | None): list of document ID, status, and type. Defaults to None.

        Returns:
            list[Message]: List of saved messages.
        """
        msg_list = [
            Message(
                id=msg.id.strip() if msg.id else "",
                conversation_id=conversation_id,
                role=msg.role,
                content=msg.content,
                created_time=datetime.now(timezone.utc),
                is_active=True,
                parent_id=msg.parent_id,
                source=msg.source,
                metadata_=attachments if msg.role == MessageRole.user else None,
            )
            for msg in message_list
        ]
        parent_id = conversation_id
        with self.db() as session:
            try:
                conversation = self._get_conversation(session, user_id, conversation_id)
                self._validate_conversation_exists(conversation_id, conversation)

                saved_messages: list[Message] = []
                for message in msg_list:
                    message_id = str(uuid.uuid4())
                    if message.id:
                        existing_message = (
                            session.query(MessageModel)
                            .filter(
                                MessageModel.id == message.id,
                                MessageModel.conversation_id == conversation_id,
                            )
                            .first()
                        )
                        if existing_message:
                            continue
                        message_id = message.id

                    metadata_text = self._serialize_metadata(message.metadata_)

                    new_message = MessageModel(
                        id=message_id,
                        conversation_id=conversation_id,
                        role=message.role,
                        content=message.content,
                        created_time=message.created_time,
                        source=message.source,
                        parent_id=message.parent_id if message.parent_id else parent_id,
                        metadata_=metadata_text,
                    )
                    conversation.updated_time = datetime.now(timezone.utc)
                    session.add(new_message)
                    session.commit()
                    parent_id = new_message.id
                    saved_messages.append(Message.model_validate(new_message))

                return saved_messages
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def get_messages_by_ids(self, message_ids: list[str], **kwargs: Any) -> list[Message]:
        """Get messages by ID.

        Args:
            message_ids (list[str]): List of message ID.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            list[Message]: List of messages.

        Raises:
            exc: SQLAlchemyError.
        """
        with self.db() as session:
            try:
                messages = session.query(MessageModel).filter(MessageModel.id.in_(message_ids)).all()
                message_list = [Message.model_validate(msg) for msg in messages]
                return message_list
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to fetch messages: {exc}")
                raise exc

    def get_message_by_id(self, message_id: str, **kwargs: Any) -> Message:
        """Get message by ID.

        Args:
            message_id (str): Message ID.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Message: Message object.
        """
        with self.db() as session:
            try:
                message = session.query(MessageModel).filter(MessageModel.id == message_id).first()
                if message:
                    message = Message.model_validate(message)
                    return message
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to fetch message: {exc}")
                raise exc

    def get_messages(
        self,
        user_id: str,
        conversation_id: str,
        limit: int | None = None,
        max_timestamp: datetime | None = None,
        **kwargs: Any,
    ) -> list[Message]:
        """Get list of messages for a conversation.

        Args:
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            limit (int): Maximum number of messages to return.
            max_timestamp (datetime): Maximum timestamp of messages to return.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            List[Message]: List of Message objects.
        """
        if not max_timestamp:
            max_timestamp = datetime.now(timezone.utc)

        with self.db() as session:
            messages = (
                session.query(MessageModel)
                .join(
                    ConversationModel,
                    MessageModel.conversation_id == ConversationModel.id,
                )
                .filter(
                    ConversationModel.id == conversation_id,
                    ConversationModel.user_id == user_id,
                    ConversationModel.is_active.is_(True),
                    MessageModel.created_time < max_timestamp,
                    MessageModel.is_active.is_(True),
                )
                .order_by(sqlalchemy.desc(MessageModel.created_time))
            )

            if limit is not None and limit >= 0:
                messages = messages.limit(limit)

            messages = messages.all()
            sorted_messages: list[Message] = sorted(messages, key=lambda x: x.created_time)

            message_list = [Message.model_validate(msg) for msg in sorted_messages]

            return message_list

    def get_last_message_by_conversation_id_and_role(
        self,
        conversation_id: str,
        role: MessageRole,
        **kwargs: Any,
    ) -> Message:
        """Retrieve the last message by conversation_id and role.

        Args:
            conversation_id (str): The ID of the conversation.
            role (MessageRole): The role of the message.
            kwargs (Any): Additional arguments.

        Returns:
            Message | None: The last message from the conversation, or None if not found.
        """
        with self.db() as session:
            try:
                message = (
                    session.query(MessageModel)
                    .join(
                        ConversationModel,
                        MessageModel.conversation_id == ConversationModel.id,
                    )
                    .filter(
                        ConversationModel.id == conversation_id,
                        ConversationModel.is_active.is_(True),
                        MessageModel.role == role,
                        MessageModel.is_active.is_(True),
                    )
                    .order_by(sqlalchemy.desc(MessageModel.created_time))
                    .first()
                )

                if message:
                    message = Message.model_validate(message)
                    return message
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to fetch last message: {exc}")
                raise exc

    def delete_messages(self, user_id: str, message_ids: list[str], chatbot_ids: list[str], **kwargs: Any) -> None:
        """Delete messages.

        Args:
            user_id (str): User ID.
            message_ids (list[str]): List of Message ID.
            chatbot_ids (list[str]): List of Chatbot ID.
            **kwargs (Any): Additional keyword arguments.
        """
        with self.db() as session:
            try:
                messages = session.query(MessageModel).filter(MessageModel.id.in_(message_ids)).all()
                for message in messages:
                    conversation = (
                        session.query(ConversationModel)
                        .filter(
                            ConversationModel.id == message.conversation_id,
                            ConversationModel.user_id == user_id,
                            ConversationModel.project_id.in_(chatbot_ids),
                        )
                        .first()
                    )
                    if conversation:
                        message.is_active = False
                        session.commit()

            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def delete_conversation(self, user_id: str, conversation_id: str, **kwargs: Any) -> None:
        """Delete conversation.

        Args:
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            **kwargs (Any): Additional keyword arguments.
        """
        with self.db() as session:
            try:
                # Delete the conversation
                conversation = (
                    session.query(ConversationModel)
                    .filter(
                        ConversationModel.id == conversation_id,
                        ConversationModel.user_id == user_id,
                    )
                    .first()
                )
                if conversation:
                    conversation.is_active = False

                # Delete all shared conversations associated with this conversation
                # Call the function directly in the same transaction
                self._delete_shared_conversation_from_conversation_in_session(session, conversation_id)

                # Commit both operations together
                session.commit()
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def _delete_shared_conversation_from_conversation_in_session(self, session: Session, conversation_id: str) -> None:
        """Helper method to delete shared conversations within an existing session.

        Args:
            session (Session): The database session to use.
            conversation_id (str): The conversation ID.
        """
        session.query(SharedConversationModel).filter(
            SharedConversationModel.conversation_id == conversation_id,
            SharedConversationModel.is_active.is_(True),
        ).update({"is_active": False})

    def delete_conversations(self, user_id: str, chatbot_id: str, **kwargs: Any) -> None:
        """Delete all conversations for a user and chatbot.

        Args:
            user_id (str): User ID.
            chatbot_id (str): Chatbot ID.
            **kwargs (Any): Additional keyword arguments.
        """
        with self.db() as session:
            try:
                conversations = (
                    session.query(ConversationModel)
                    .filter(
                        ConversationModel.user_id == user_id,
                        ConversationModel.project_id == chatbot_id,
                        ConversationModel.is_active.is_(True),
                    )
                    .all()
                )

                for conversation in conversations:
                    conversation.is_active = False

                session.commit()
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def save_feedback(self, user_id: str, message_id: str, feedback: str | None, **kwargs: Any) -> None:
        """Save feedback.

        Args:
            user_id (str): User ID.
            message_id (str): Message ID.
            feedback (str | None): Feedback data.
            **kwargs (Any): Additional keyword arguments.
        """
        with self.db() as session:
            try:
                message = session.query(MessageModel).filter(MessageModel.id == message_id).first()
                if message:
                    conversation = (
                        session.query(ConversationModel).filter(ConversationModel.id == message.conversation_id).first()
                    )
                    if conversation and conversation.user_id == user_id:
                        message.feedback = feedback
                        session.commit()
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def create_conversation_document(
        self,
        conversation_id: str,
        status: str = DocumentStatus.PROCESSING.value,
        file_hash: str = "",
        **kwargs: Any,
    ) -> ConversationDocument:
        """Create new conversation document.

        Args:
            conversation_id (str): Conversation ID.
            status (str): Document status.
            file_hash (str): File hash.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            ConversationDocument: Newly created ConversationDocument object.
        """
        with self.db() as session:
            try:
                document = ConversationDocumentModel(
                    id=f"{conversation_id}-{file_hash}",
                    conversation_id=conversation_id,
                    status=self._str_to_status(status),
                )
                session.add(document)
                session.commit()

                new_document = ConversationDocument.model_validate(document)
                return new_document
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def get_conversation_document(self, document_id: str, **kwargs: Any) -> ConversationDocument:
        """Get conversation document.

        Args:
            document_id (str): Document ID.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            ConversationDocument: ConversationDocument object.
        """
        with self.db() as session:
            try:
                document = (
                    session.query(ConversationDocumentModel).filter(ConversationDocumentModel.id == document_id).first()
                )
                if document:
                    document = ConversationDocument.model_validate(document)
                    return document
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def get_message_stats(self, start_date: datetime, end_date: datetime) -> dict[str, int]:
        """Get message statistics within a date range.

        Args:
            start_date (datetime): Start date for the statistics.
            end_date (datetime): End date for the statistics.

        Returns:
            dict[str, int]: Dictionary containing message statistics including:
                - total_messages: Total number of messages
                - thumbs_up_count: Count of positive feedback
                - thumbs_down_count: Count of negative feedback
                - Detailed breakdown of thumbs down reasons

        Raises:
            ValueError: If the input dates are invalid
            SQLAlchemyError: If there's a database-related error
        """
        self._validate_date_parameters(start_date, end_date)

        with self.db() as session:
            try:
                return self._execute_message_stats_query(session, start_date, end_date)
            except SQLAlchemyError as exc:
                logger.warning("Failed to fetch message statistics: %s", exc)
                raise exc
            except Exception as general_exc:
                logger.warning("Unexpected error in get_message_stats: %s", general_exc)
                raise general_exc

    def _validate_date_parameters(self, start_date: datetime, end_date: datetime) -> None:
        """Validate the date parameters for message stats query.

        Args:
            start_date (datetime): Start date for the statistics.
            end_date (datetime): End date for the statistics.

        Raises:
            ValueError: If dates are invalid or in wrong order
        """
        if not isinstance(start_date, datetime) or not isinstance(end_date, datetime):
            raise ValueError("Start date and end date must be datetime objects")

        if start_date > end_date:
            raise ValueError("Start date cannot be after end date")

    def _execute_message_stats_query(
        self, session: Session, start_date: datetime, end_date: datetime
    ) -> dict[str, int]:
        """Execute the SQL query for message statistics and process the results.

        Args:
            session (Session): Database session
            start_date (datetime): Start date for the statistics
            end_date (datetime): End date for the statistics

        Returns:
            dict[str, int]: Dictionary of message statistics

        Raises:
            SQLAlchemyError: If there's a database-related error
        """
        stats_query = self._build_message_stats_query(FEEDBACK_REASON_CATEGORIES)

        try:
            result_proxy = session.execute(
                sqlalchemy.text(stats_query),
                {"start_date": start_date, "end_date": end_date},
            )
        except sqlalchemy.exc.SQLAlchemyError as sql_err:
            logger.warning("SQL execution error in message stats: %s", sql_err)
            raise SQLAlchemyError(f"Failed to execute SQL query: {sql_err}") from sql_err

        return self._process_stats_results(result_proxy, FEEDBACK_REASON_CATEGORIES)

    def _build_message_stats_query(self, reason_categories: list[str]) -> str:
        """Build the SQL query for message statistics.

        Args:
            reason_categories (list[str]): List of reason categories

        Returns:
            str: SQL query string
        """
        # Base SQL for message counts
        base_sql = """
        SELECT
            COUNT(DISTINCT id) as total_messages,
            COUNT(DISTINCT CASE WHEN feedback::json->>'type' = 'good' THEN id END) as thumbs_up_count,
            COUNT(DISTINCT CASE WHEN feedback::json->>'type' = 'bad' THEN id END) as thumbs_down_count,
        """

        # Add each reason count to the SQL
        reason_counts_sql = self._build_reason_counts_sql(reason_categories)

        # Add the other reasons count
        not_in_list = ", ".join([f"'{reason}'" for reason in reason_categories])
        other_reasons_sql = f"""
            COUNT(DISTINCT CASE WHEN feedback::json->>'type' = 'bad' AND
                feedback::json->>'reason' NOT IN ({not_in_list}) AND
                feedback::json->>'reason' IS NOT NULL
            THEN id END) as other_reasons_count
        FROM message
        WHERE created_time BETWEEN :start_date AND :end_date
            AND is_active = true
        """

        return base_sql + reason_counts_sql + other_reasons_sql

    def _build_reason_counts_sql(self, reason_categories: list[str]) -> str:
        """Build the SQL fragment for counting each feedback reason.

        Args:
            reason_categories (list[str]): List of reason categories

        Returns:
            str: SQL fragment for counting each reason
        """
        reason_counts_sql = ""
        for reason in reason_categories:
            reason_tag = self._reason_to_field_name(reason)
            reason_counts_sql += f"""
            COUNT(DISTINCT CASE WHEN feedback::json->>'type' = 'bad' AND
                feedback::json->>'reason' = '{reason}'
                THEN id END) as {reason_tag}_count,
            """
        return reason_counts_sql

    def _reason_to_field_name(self, reason: str) -> str:
        """Convert a reason category to a valid field name.

        Args:
            reason (str): Reason category string

        Returns:
            str: Field name for the reason
        """
        return (
            reason.lower()
            .replace(" ", "_")
            .replace("''", "")  # Double apostrophes in SQL become empty
            .replace("-", "_")
        )

    def _process_stats_results(self, result_proxy: Any, reason_categories: list[str]) -> dict[str, int]:
        """Process the query results into a stats dictionary.

        Args:
            result_proxy (Any): SQLAlchemy result proxy (can be ResultProxy or Result
                                depending on SQLAlchemy version)
            reason_categories (list[str]): List of reason categories

        Returns:
            dict[str, int]: Dictionary of message statistics
        """
        # Initialize with empty stats dictionary
        stats_dict = self._initialize_stats_dict(reason_categories)

        try:
            result = result_proxy.first()
            if result:
                # Safely access columns by index or through mapping
                for idx, column in enumerate(result_proxy.keys()):
                    stats_dict[column] = result[idx] or 0
        except Exception as fetch_err:
            logger.warning("Error mapping results to stats dictionary: %s", fetch_err)
            # Continue with default values if mapping fails

        return stats_dict

    def _initialize_stats_dict(self, reason_categories: list[str]) -> dict[str, int]:
        """Initialize an empty stats dictionary with zero values.

        Args:
            reason_categories (list[str]): List of reason categories

        Returns:
            dict[str, int]: Empty stats dictionary with zero values
        """
        stats_dict = {
            "total_messages": 0,
            "thumbs_up_count": 0,
            "thumbs_down_count": 0,
        }

        # Add all reason stats with zero values
        for reason in reason_categories:
            reason_tag = self._reason_to_field_name(reason)
            stats_dict[f"{reason_tag}_count"] = 0

        stats_dict["other_reasons_count"] = 0

        return stats_dict

    def update_conversation_document(
        self,
        document_id: str,
        status: str,
        number_of_chunks: int,
        message: str | None,
        object_key: str | None,
        **kwargs: Any,
    ) -> ConversationDocument:
        """Update conversation document status.

        Args:
            document_id (str): Document ID.
            status (str): Document status.
            number_of_chunks (int): The number of chunks.
            message (str | None): The message passed from the document processing. Defaults to None.
            object_key (str | None): The object key. Defaults to None.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            ConversationDocument: Updated ConversationDocument object.
        """
        with self.db() as session:
            try:
                document = (
                    session.query(ConversationDocumentModel).filter(ConversationDocumentModel.id == document_id).first()
                )
                if document:
                    document.status = self._str_to_status(status)
                    document.number_of_chunks = number_of_chunks
                    document.message = message
                    if object_key:
                        document.object_key = object_key
                    session.commit()

                    updated_document = ConversationDocument.model_validate(document)
                    return updated_document
                raise ValueError(f"Document id {document_id} does not exist.")
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def get_deanonymized_message(  # noqa: PLR0913
        self,
        user_id: str,
        conversation_id: str,
        message_id: str,
        is_anonymized: bool,
        mappings: list[AnonymizerMapping],
        **kwargs: Any,
    ) -> Message:
        """Get a deanonymized message for a specific user and message ID.

        Args:
            user_id (str): User ID.
            conversation_id (str): Conversation ID.
            message_id (str): Message ID.
            is_anonymized (bool): Flag to indicate whether the message is anonymized.
            mappings (list[AnonymizerMapping]): List of AnonymizerMapping objects.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Message: The retrieved Message object.

        Raises:
            ValueError: If no message is found with the specified message ID.
        """
        with self.db() as session:
            message = (
                session.query(MessageModel)
                .join(
                    ConversationModel,
                    MessageModel.conversation_id == ConversationModel.id,
                )
                .filter(
                    ConversationModel.user_id == user_id,
                    MessageModel.id == message_id,
                    MessageModel.conversation_id == conversation_id,
                )
                .first()
            )

            if message:
                message_model = Message.model_validate(message)
                return self._deanonymize_message(message_model, is_anonymized, mappings)
            else:
                raise ValueError(f"Message id {message_id} does not exist.")

    def get_deanonymized_messages(
        self,
        messages: list[Message],
        is_anonymized: bool,
        mappings: list[AnonymizerMapping] | None = None,
        **kwargs: Any,
    ) -> list[Message]:
        """Delegate message deanonymization processing to the repository.

        This method forwards the messages and mappings to a repository method
        that handles the actual deanonymization.

        Args:
            messages (list[Message]): List of messages to be anonymized.
            is_anonymized (bool): Flag to indicate whether the messages are anonymized.
            mappings (list[AnonymizerMapping] | None): Anonymizer mappings used to deanonymize message content.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            list[Message]: List of messages with deanonymized content.
        """
        message_list = []
        for msg in messages:
            message_list.append(self._deanonymize_message(msg, is_anonymized, mappings))
        return message_list

    def get_deanonymized_texts(
        self,
        texts: list[str],
        is_anonymized: bool,
        mappings: list[AnonymizerMapping] | None = None,
    ) -> list[str]:
        """Retrieve the deanonymized version of the given text.

        This function uses an anonymizer tool to replace anonymized placeholders
        in the text with original values based on provided mappings.

        Args:
            texts (list[str]): The anonymized texts to be processed.
            is_anonymized (bool): Flag to determine if the text is anonymized.
            mappings (list[AnonymizerMapping] | None): A list of mappings for deanonymization.

        Returns:
            list[str]: The deanonymized texts.
        """
        return [self._get_deanonymized_text(text, is_anonymized, mappings) for text in texts]

    def _deanonymize_message(
        self,
        message: Message,
        is_anonymized: bool,
        mappings: list[AnonymizerMapping] | None = None,
    ) -> Message:
        """Process deanonymize message.

        Args:
            message (Message): Message to process.
            is_anonymized (bool): Flag to determine if the messages are anonymized.
            mappings (list[AnonymizerMapping] | None): Anonymizer mappings used to deanonymize message content.

        Returns:
            Message: Message with deanonymized content.
        """
        deanonymized_text = self._get_deanonymized_text(message.content, is_anonymized, mappings)
        message.deanonymized_content = deanonymized_text

        if message.metadata_:
            self._validate_and_normalize_metadata(message)

            if "references" in message.metadata_:
                for reference in message.metadata_["references"]:
                    if "content" in reference:
                        reference["content"] = self._get_deanonymized_text(
                            reference["content"], is_anonymized, mappings
                        )
            if "related" in message.metadata_:
                message.metadata_["related"] = [
                    self._get_deanonymized_text(question, is_anonymized, mappings)
                    for question in message.metadata_["related"]
                ]
        return message

    def _validate_and_normalize_metadata(self, message: Message) -> None:
        """Ensure the metadata is valid.

        Args:
            message (Message): Message to ensure metadata validity.
        """
        if isinstance(message.metadata_, str):
            try:
                message.metadata_ = json.loads(message.metadata_)
            except json.JSONDecodeError as e:
                raise json.JSONDecodeError(
                    f"Failed to parse metadata: {message.metadata_}", message.metadata_, 0
                ) from e

        message.metadata_ = self._normalize_attachment_metadata(message.id, message.metadata_)

    def _normalize_attachment_metadata(self, message_id: str, metadata: dict[str, Any]) -> dict[str, Any]:
        """Fix nested attachment structure: {"attachments": {"attachments": [...]}} -> {"attachments": [...]}.

        The nested structure may be caused by the attachment metadata being stored as a dictionary
        with a key "attachments" that contains a list of attachments (not the correct structure).

        Args:
            message_id (str): Message ID.
            metadata (dict[str, Any]): Metadata dictionary.

        Returns:
            dict[str, Any]: Normalized metadata dictionary.
        """
        if not isinstance(metadata, dict) or "attachments" not in metadata:
            logger.debug("No attachments found in metadata, returning original metadata.")
            return metadata

        attachments = metadata["attachments"]

        # Check for nested structure
        if isinstance(attachments, dict) and "attachments" in attachments:
            logger.warning(
                "Found nested attachment structure in metadata for message_id=%s: %s", message_id, attachments
            )

            # Flatten the structure
            metadata = metadata.copy()
            metadata["attachments"] = attachments["attachments"]

            logger.info(
                "Fixed nested attachment structure in metadata for message_id=%s. New structure: %s",
                message_id,
                metadata["attachments"],
            )

        return metadata

    def update_message_metadata(self, message_id: str, metadata_: dict[str, Any], **kwargs: Any) -> Message:
        """Update message metadata.

        Args:
            message_id (str): Message ID.
            metadata_ (dict[str, Any]): Metadata to be updated.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            Message: Updated Message object.
        """
        with self.db() as session:
            try:
                message = session.query(MessageModel).filter(MessageModel.id == message_id).first()
                if message:
                    message.metadata_ = self._serialize_metadata(metadata_)
                    session.commit()

                    updated_message = Message.model_validate(message)
                    return updated_message
                raise ValueError(f"Message id {message_id} does not exist.")
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def _get_deanonymized_text(
        self,
        text: str,
        is_anonymized: bool,
        mappings: list[AnonymizerMapping] | None = None,
    ) -> str:
        """Retrieve the deanonymized version of the given text.

        This function uses an anonymizer tool to replace anonymized placeholders
        in the text with original values based on provided mappings.

        Args:
            text (str): The anonymized text to be processed.
            is_anonymized (bool): Flag to determine if the text is anonymized.
            mappings (list[AnonymizerMapping]): A list of mappings for deanonymization.

        Returns:
            str: The deanonymized text.
        """
        if not mappings or not is_anonymized:
            return text

        try:
            mapping_data_type = AnonymizerMapping.convert_to_mapping_data_type(mappings)
            anonymizer = TextAnonymizer(
                text_analyzer=self.text_analyzer,
                deanonymizer_mapping=DeanonymizerMapping(copy.deepcopy(mapping_data_type)),
            )
            return anonymizer.deanonymize(text)
        except Exception as e:
            logger.warning(f"Failed to decrypt PII value, falling back to anonymized value: {e}")
            return text

    def _get_conversation(self, session: Session, user_id: str, conversation_id: str) -> ConversationModel | None:
        """Get conversation model by ID.

        Args:
            session (Session): SQLAlchemy session.
            user_id (str): User ID.
            conversation_id (str): ConversationModel ID.

        Returns:
            ConversationModel | None: Conversation object.
        """
        conversation = (
            session.query(ConversationModel)
            .filter(
                ConversationModel.user_id == user_id,
                ConversationModel.id == conversation_id,
                ConversationModel.is_active.is_(True),
            )
            .first()
        )
        return conversation

    def _str_to_status(self, status_str: str) -> DocumentStatus:
        """Convert string status to DocumentStatus enum.

        Args:
            status_str (str): Document status.

        Returns:
            DocumentStatus: Document status enum.
        """
        try:
            return DocumentStatus[status_str.upper()]
        except KeyError:
            return DocumentStatus.PROCESSING

    def _validate_conversation_exists(self, conversation_id: str, conversation: ConversationModel | None) -> None:
        """Validate if conversation exists.

        Args:
            conversation_id (str): ConversationModel ID.
            conversation (ConversationModel | None): ConversationModel object

        Raises:
            ValueError: If conversation does not exist.
        """
        if not conversation:
            raise ValueError(f"Conversation id {conversation_id} does not exist.")

    def _serialize_metadata(self, metadata: Any) -> str | None:
        """Serialize metadata dictionary to JSON string.

        Args:
            metadata (Any): Metadata object.

        Returns:
            str | None: JSON string representation of metadata.
        """
        return json.dumps(metadata) if metadata is not None else None

    def create_shared_conversation(
        self,
        id: str,
        user_id: str,
        conversation_id: str,
        now: datetime,
        expiry_days: int | None = SharedConversationConstants.DEFAULT_EXPIRY_DAYS,
    ) -> SharedConversation:
        """Create a shared conversation access ID.

        Args:
            id (str): The UUID to access the shared conversation.
            user_id (str): The user ID.
            conversation_id (str): The conversation ID.
            expiry_days (int | None): Number of days until link expires. Defaults to None (no expiry)
            now (datetime): The time the shared conversation was created.

        Returns:
            SharedConversation: The created shared conversation access ID.
        """
        with self.db() as session:  # pylint: disable=not-callable
            try:
                expired_time = now + timedelta(days=expiry_days) if expiry_days is not None else None
                shared_conversation = SharedConversationModel(
                    id=id,
                    user_id=user_id,
                    conversation_id=conversation_id,
                    created_time=now,
                    expired_time=expired_time,
                    last_updated_time=now,
                    is_active=True,
                )
                session.add(shared_conversation)
                session.commit()
                session.refresh(shared_conversation)

                return SharedConversation.model_validate(shared_conversation)
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to create shared conversation: {exc}")
                session.rollback()
                raise exc

    def get_shared_conversations(self, user_id: str, query: str | None) -> list[dict[str, Any]]:
        """Get list of shared conversations with titles for a user.

        Args:
            user_id (str): User ID.
            query (str | None): Search query for conversation title. If None, no filter will be applied.

        Returns:
            list[dict[str, Any]]: List of shared conversations with titles and matching words.
                Returns empty list if no conversations are found.

        Raises:
            ValueError: If database operation fails.
        """
        try:
            with self.db() as session:
                base_query = (
                    session.query(SharedConversationModel, ConversationModel.title)
                    .outerjoin(ConversationModel, SharedConversationModel.conversation_id == ConversationModel.id)
                    .filter(SharedConversationModel.user_id == user_id)
                    .filter(SharedConversationModel.is_active.is_(True))
                )

                base_query = base_query.filter(
                    or_(
                        SharedConversationModel.expired_time.is_(None),
                        SharedConversationModel.expired_time > datetime.now(timezone.utc),
                    )
                )

                if query:
                    base_query = base_query.filter(ConversationModel.title.ilike(f"%{query}%"))

                base_query = base_query.order_by(desc(SharedConversationModel.last_updated_time))

                results = base_query.all()
                if not results:
                    return []

                shared_conversations_with_titles: list[dict[str, Any]] = []
                for shared_conv, title in results:
                    shared_conv_dict: dict[str, Any] = {
                        "id": shared_conv.id,
                        "user_id": shared_conv.user_id,
                        "conversation_id": shared_conv.conversation_id,
                        "created_time": shared_conv.created_time,
                        "last_updated_time": shared_conv.last_updated_time,
                        "expired_time": shared_conv.expired_time,
                        "title": title or "",
                        "first_matching_word": self.find_query_in_title(title, query) if query and title else None,
                    }
                    shared_conversations_with_titles.append(shared_conv_dict)

                return shared_conversations_with_titles

        except SQLAlchemyError as e:
            logger.warning(f"Database error while fetching shared conversations with titles: {e}")
            raise ValueError("Failed to fetch shared conversations with titles") from e

    def find_query_in_title(self, title: str, query: str) -> str | None:
        """Find the first word or phrase in the title that contains the query.

        This performs case-insensitive substring matching and returns either:
        - The first word containing the query
        - Or a phrase (consecutive characters) that matches across words

        Args:
            title (str): The conversation title.
            query (str): The search query.

        Returns:
            str | None: The first matching word or phrase, or None if no match found.
        """
        title = title.strip()
        query = query.strip()
        if not title or not query:
            return None

        title_lower = title.lower()
        query_lower = query.lower()

        idx = title_lower.find(query_lower)
        if idx == -1:
            return None

        # Expand left to start of word
        start = idx
        while start > 0 and title[start - 1] != " ":
            start -= 1

        # Expand right to end of word(s)
        end = idx + len(query)
        while end < len(title) and title[end] != " ":
            end += 1

        return title[start:end].strip().lower()

    def get_shared_conversation_by_shared_conversation_id(
        self, shared_conversation_id: str, **kwargs: Any
    ) -> SharedConversation | None:
        """Get a shared conversation by shared conversation ID.

        Args:
            shared_conversation_id (str): The shared conversation access ID.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            SharedConversation | None: The shared conversation details if found based on the access ID.
        """
        with self.db() as session:
            shared_conversation = (
                session.query(SharedConversationModel)
                .filter(SharedConversationModel.id == shared_conversation_id)
                .filter(SharedConversationModel.is_active.is_(True))
                .first()
            )
            return SharedConversation.model_validate(shared_conversation) if shared_conversation else None

    def get_shared_conversation_by_conversation_id(
        self, conversation_id: str, **kwargs: Any
    ) -> SharedConversation | None:
        """Get all shared conversations for a specific conversation.

        Args:
            conversation_id (str): The conversation ID.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            SharedConversation | None: The shared conversation for the conversation. None if not found.
        """
        with self.db() as session:
            try:
                shared_conversation = (
                    session.query(SharedConversationModel)
                    .filter(SharedConversationModel.conversation_id == conversation_id)
                    .filter(SharedConversationModel.is_active.is_(True))
                    .filter(
                        or_(
                            SharedConversationModel.expired_time.is_(None),
                            SharedConversationModel.expired_time > datetime.now(timezone.utc),
                        )
                    )
                    .first()
                )

                if shared_conversation:
                    return SharedConversation.model_validate(shared_conversation)
                return None
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to get shared conversation by conversation id: {exc}")
                raise exc

    def update_shared_conversation(
        self,
        shared_conversation_id: str,
        last_updated_time: datetime,
        expired_time: datetime | None = None,
        is_active: bool = True,
    ) -> SharedConversation | None:
        """Update a shared conversation.

        Args:
            shared_conversation_id (str): The shared conversation ID.
            last_updated_time (datetime | None): New last updated time.
            expired_time (datetime | None): New expiry time, if provided.
            is_active (bool): New is_active value.

        Returns:
            SharedConversation | None: The updated shared conversation, None if not found.
        """
        with self.db() as session:
            try:
                shared_conversation = (
                    session.query(SharedConversationModel)
                    .filter(SharedConversationModel.id == shared_conversation_id)
                    .filter(SharedConversationModel.is_active.is_(True))
                    .first()
                )
                if shared_conversation:
                    shared_conversation.expired_time = expired_time
                    shared_conversation.last_updated_time = last_updated_time
                    shared_conversation.is_active = is_active
                    session.commit()
                    session.refresh(shared_conversation)
                    return SharedConversation.model_validate(shared_conversation)
                return None
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to update shared conversation: {exc}")
                session.rollback()
                raise exc

    def delete_shared_conversation(self, shared_conversation_id: str, user_id: str) -> None:
        """Soft delete a shared conversation.

        Args:
            shared_conversation_id (str): The shared conversation ID.
            user_id (str): The user ID.
        """
        with self.db() as session:
            try:
                shared_conversation = (
                    session.query(SharedConversationModel)
                    .filter(SharedConversationModel.id == shared_conversation_id)
                    .filter(SharedConversationModel.user_id == user_id)
                    .filter(SharedConversationModel.is_active.is_(True))
                    .first()
                )
                if shared_conversation:
                    shared_conversation.is_active = False
                    session.commit()
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to delete the shared conversation: {exc}")
                session.rollback()
                raise exc

    def clone_conversation_document(
        self,
        new_file_id: str,
        target_conversation_id: str,
        original_document: ConversationDocument,
        object_key: str,
        **kwargs: Any,
    ) -> ConversationDocument:
        """Clone a conversation document with new ID and conversation ID.

        Args:
            new_file_id (str): The new file ID for the cloned document.
            target_conversation_id (str): The target conversation ID.
            original_document (ConversationDocument): The original document to clone.
            object_key (str): The object key for the cloned document.
            **kwargs (Any): Additional keyword arguments.

        Returns:
            ConversationDocument: The newly created ConversationDocument object.

        Raises:
            SQLAlchemyError: If database operation fails.
        """
        with self.db() as session:
            try:
                new_doc = ConversationDocumentModel(
                    id=new_file_id,
                    conversation_id=target_conversation_id,
                    status=original_document.status,
                    number_of_chunks=original_document.number_of_chunks,
                    message=original_document.message,
                    object_key=object_key,
                )
                session.add(new_doc)
                session.commit()
                session.refresh(new_doc)

                return ConversationDocument.model_validate(new_doc)
            except SQLAlchemyError as exc:
                logger.warning(f"Failed to clone conversation document: {exc}")
                session.rollback()
                raise exc
