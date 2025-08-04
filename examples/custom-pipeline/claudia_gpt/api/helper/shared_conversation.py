"""This module contains the helper functions for shared conversations.

Authors:
    Felicia Limanta (felicia.limanta@gdplabs.id)

References:
    None
"""

import copy
from datetime import datetime, timedelta, timezone
from http import HTTPStatus
from typing import TYPE_CHECKING, Any, NamedTuple
from uuid import uuid4

from bosa_core import PluginManager
from fastapi import HTTPException
from glchat_plugin.pipeline.pipeline_handler import PipelineHandler

from claudia_gpt.anonymizer.anonymizer_storage import AnonymizerStorage
from claudia_gpt.api.model.response import SharedConversationResponse
from claudia_gpt.chat_history.chat_history_storage import ChatHistoryStorage
from claudia_gpt.chat_history.constants import ChatHistoryConstants
from claudia_gpt.chat_history.schemas import SharedConversation
from claudia_gpt.config.constant import ConversationConstants, SharedConversationConstants
from claudia_gpt.utils.logger import logger

if TYPE_CHECKING:
    from claudia_gpt.chat_history.schemas import Message


class SharedConversationSetupResult(NamedTuple):
    """Result of setting up a shared conversation continuation."""

    new_conversation_id: str
    cloned_messages: list["Message"]
    chatbot_id: str
    message_id_mapping: dict[str, str]


class SharedConversationManager:
    """Class to manage shared conversations."""

    def __init__(self, chat_history_storage: ChatHistoryStorage):
        """Initialize the SharedConversationManager.

        Args:
            chat_history_storage (ChatHistoryStorage): The chat history storage instance.
        """
        self.chat_history_storage = chat_history_storage

    def _validate_shared_conversation(
        self,
        shared_conversation: SharedConversation | None,
        shared_conversation_id: str,
        user_id: str | None = None,
        check_ownership: bool = False,
    ) -> None:
        """Validate shared conversation with flexible ownership checking.

        Args:
            shared_conversation: The shared conversation object or None
            shared_conversation_id: The shared conversation ID for error messages
            user_id: The user ID to check ownership against (if check_ownership=True)
            check_ownership: Whether to validate user ownership

        Raises:
            HTTPException: If validation fails
        """
        if shared_conversation is None:
            logger.info(f"Shared conversation {shared_conversation_id} does not exist.")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SharedConversationConstants.ERR_NOT_FOUND_MSG)

        if check_ownership and user_id and shared_conversation.user_id != user_id:
            logger.info(f"Shared conversation {shared_conversation_id} is not owned by user {user_id}.")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SharedConversationConstants.ERR_NOT_FOUND_MSG)

        if not shared_conversation.is_active:
            logger.info(f"Shared conversation {shared_conversation_id} is deleted.")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SharedConversationConstants.ERR_NOT_FOUND_MSG)

        if shared_conversation.expired_time and shared_conversation.expired_time < datetime.now(timezone.utc):
            logger.info(f"Shared conversation {shared_conversation_id} has expired.")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SharedConversationConstants.ERR_NOT_FOUND_MSG)

    def _validate_user_access(self, user_id: str, shared_conversation_id: str) -> None:
        """Validate if the user has access to the shared conversation.

        Args:
            user_id (str): The user ID.
            shared_conversation_id (str): The shared conversation ID.
        """
        shared_conversation = self.chat_history_storage.get_shared_conversation_by_shared_conversation_id(
            shared_conversation_id
        )
        self._validate_shared_conversation(shared_conversation, shared_conversation_id, user_id, check_ownership=True)

    def create_or_update_shared_conversation_access(
        self,
        user_id: str,
        conversation_id: str,
        expiry_days: int | None = SharedConversationConstants.DEFAULT_EXPIRY_DAYS,
    ) -> SharedConversationResponse:
        """Create or reuse a shared conversation id.

        Args:
            user_id (str): The user ID.
            conversation_id (str): The conversation ID.
            expiry_days (int | None): Number of days until link expires. Defaults to None (no expiry).

        Returns:
            SharedConversationResponse: The share ID, expiry time.
        """
        if expiry_days is not None and expiry_days <= 0:
            logger.info(
                "Attempted to create a shared conversation with a non-positive expiry days. Raising ValueError."
            )
            raise ValueError("Expiry days must be a positive number")

        conversation = self.chat_history_storage.get_conversation(user_id, conversation_id)

        if not conversation or conversation.user_id != user_id:
            logger.info(f"Conversation {conversation_id} not found.")
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=ConversationConstants.ERR_NOT_FOUND_MSG)

        # create a new shared conversation if it doesn't exist
        now: datetime = datetime.now(timezone.utc)

        messages = self.chat_history_storage.get_messages(
            user_id=user_id,
            conversation_id=conversation_id,
            max_timestamp=now,
        )
        if not messages:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN, detail=SharedConversationConstants.ERR_EMPTY_CONVERSATION_MSG
            )

        active_shared_conversation = self.get_active_shared_conversation(conversation_id)

        if active_shared_conversation:
            updated_shared_conversation = self._update_existing_shared_conversation(
                active_shared_conversation, expiry_days, now, user_id, conversation_id
            )
        else:
            updated_shared_conversation = self._create_new_shared_conversation(
                user_id, conversation_id, expiry_days, now
            )

        return SharedConversationResponse(
            shared_conversation_id=updated_shared_conversation.id,
            last_updated_time=updated_shared_conversation.last_updated_time,
            expired_time=updated_shared_conversation.expired_time,
            # is_active=updated_shared_conversation.is_active,
        )

    def get_active_shared_conversation(self, conversation_id: str) -> SharedConversation | None:
        """Get active shared conversations for a conversation.

        Args:
            conversation_id (str): The conversation ID.

        Returns:
            SharedConversation | None: The active shared conversation. None if not found.
        """
        existing_shared_conversation: SharedConversation | None = (
            self.chat_history_storage.get_shared_conversation_by_conversation_id(conversation_id)
        )
        return existing_shared_conversation

    def _update_existing_shared_conversation(
        self,
        shared_conversation: SharedConversation,
        expiry_days: int | None,
        now: datetime,
        user_id: str,
        conversation_id: str,
    ) -> SharedConversation:
        """Update an existing shared conversation.

        Args:
            shared_conversation (SharedConversation): The existing shared conversation.
            expiry_days (int | None): Number of days until link expires.
            now (datetime): Current time.
            user_id (str): The user ID.
            conversation_id (str): The conversation ID.

        Returns:
            SharedConversation: The updated shared conversation.

        Raises:
            HTTPException: If update fails.
        """
        self._validate_user_access(user_id, shared_conversation.id)

        expired_time = now + timedelta(days=expiry_days) if expiry_days is not None else None

        try:
            updated_shared_conversation = self.chat_history_storage.update_shared_conversation(
                shared_conversation_id=shared_conversation.id,
                expired_time=expired_time,
                last_updated_time=now,
            )

            if updated_shared_conversation is None:
                logger.warning(
                    f"Failed to update shared conversation {shared_conversation.id} for "
                    f"conversation {shared_conversation.conversation_id}. Update returned None."
                )
                raise HTTPException(
                    status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Failed to update shared conversation link"
                )

            logger.info(
                f"Reusing shared conversation {updated_shared_conversation.id} for user {user_id} and "
                f"conversation {conversation_id} with expired time of {updated_shared_conversation.expired_time}."
            )
            return updated_shared_conversation
        except Exception as e:
            logger.warning(
                f"Failed to update shared conversation {shared_conversation.id} for "
                f"conversation {shared_conversation.conversation_id}: {str(e)}"
            )
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR, detail="Failed to update shared conversation link"
            ) from e

    def _create_new_shared_conversation(
        self, user_id: str, conversation_id: str, expiry_days: int | None, now: datetime
    ) -> SharedConversation:
        """Create a new shared conversation.

        Args:
            user_id (str): The user ID.
            conversation_id (str): The conversation ID.
            expiry_days (int | None): Number of days until link expires.
            now (datetime): The time the shared conversation was created.

        Returns:
            SharedConversation: The new shared conversation.
        """
        shared_conversation_id = str(uuid4())

        shared_conversation: SharedConversation = self.chat_history_storage.create_shared_conversation(
            id=shared_conversation_id,
            user_id=user_id,
            conversation_id=conversation_id,
            now=now,
            expiry_days=expiry_days,
        )

        logger.info(
            f"Shared conversation {shared_conversation_id} created by user {user_id} for "
            f"conversation {conversation_id} with expiry days of {expiry_days}."
        )

        return shared_conversation

    def get_shared_conversation(self, shared_conversation_id: str) -> SharedConversation:
        """Get a shared conversation.

        Args:
            shared_conversation_id (str): The shared conversation access ID.

        Returns:
            SharedConversation: The validated shared conversation details.

        Raises:
            HTTPException: If the shared conversation access id is invalid, inactive, or expired.
        """
        shared_conversation = self.chat_history_storage.get_shared_conversation_by_shared_conversation_id(
            shared_conversation_id
        )
        self._validate_shared_conversation(shared_conversation, shared_conversation_id)
        return shared_conversation

    def get_shared_conversations(self, user_id: str, query: str | None = None) -> list[SharedConversation]:
        """Get all shared conversations of a user.

        Args:
            user_id (str): The user ID.
            query (str | None): Search query for conversation title.
                                If None, no filter will be applied.

        Returns:
            list[SharedConversation]: The shared conversations.

        Raises:
            HTTPException: If no shared conversations are found
                           or the user does not have access to the shared conversation
        """
        shared_conversations = self.chat_history_storage.get_shared_conversations(user_id=user_id, query=query)

        return shared_conversations

    def delete_shared_conversation(self, shared_conversation_id: str, user_id: str) -> None:
        """Delete a shared conversation by inactivating it, ensuring the user owns it.

        Args:
            shared_conversation_id (str): The shared conversation ID.
            user_id (str): The ID of the user attempting to delete the shared conversation.

        Raises:
            HTTPException: If the shared conversation is not found, or if the user
                           is not authorized to delete it.
        """
        self._validate_user_access(user_id, shared_conversation_id)

        self.chat_history_storage.delete_shared_conversation(shared_conversation_id, user_id)
        logger.info(f"Shared conversation {shared_conversation_id} owned by user {user_id} has been deleted.")

    def get_shared_conversation_id_by_conversation_id(self, conversation_id: str) -> str | None:
        """Get the shared conversation ID for a given conversation ID.

        Args:
            conversation_id (str): The conversation ID.

        Returns:
            str | None: The shared conversation ID if found, None otherwise.
        """
        shared_conversation = self.get_active_shared_conversation(conversation_id)
        return shared_conversation.id if shared_conversation else None

    def clone_message_attachments(
        self,
        source_conversation_id: str,
        target_conversation_id: str,
        attachments: list[dict[str, Any]],
        attachment_id_mapping: dict[str, str],
    ) -> list[dict[str, Any]]:
        """Clone attachments using Minio copy_object.

        Args:
            source_conversation_id (str): The ID of the source conversation containing the original attachments.
            target_conversation_id (str): The ID of the target conversation where attachments will be cloned.
            attachments (list[dict[str, Any]]): List of attachment dictionaries containing file information.
            attachment_id_mapping (dict[str, str]): Mapping of old file IDs to new file IDs to track cloned files.

        Returns:
            list[dict[str, Any]]: List of cloned attachment dictionaries with updated file IDs.
        """
        from claudia_gpt.api.helper.object_storage import ObjectStorageHelper

        object_storage_helper = ObjectStorageHelper.get_instance()
        cloned_attachments = []

        for attachment in attachments:
            if "id" not in attachment or not attachment["id"]:
                logger.warning(f"Attachment missing an 'id' field, skipping: {attachment}")
                continue

            old_file_id = str(attachment["id"])
            if old_file_id in attachment_id_mapping:
                # Already cloned, reuse
                new_file_id = attachment_id_mapping[old_file_id]
                cloned_attachment = copy.deepcopy(attachment)
                cloned_attachment["id"] = new_file_id
                cloned_attachments.append(cloned_attachment)
                continue

            original_document = self.chat_history_storage.get_conversation_document(old_file_id)
            if not original_document:
                logger.warning(f"Original document not found for attachment {old_file_id}, skipping")
                continue

            new_file_id = str(uuid4())
            source_key = f"{source_conversation_id}/{old_file_id}"
            target_key = f"{target_conversation_id}/{new_file_id}"

            try:
                object_storage_helper.copy_object(source_key, target_key)
                self.chat_history_storage.clone_conversation_document(
                    new_file_id=new_file_id,
                    target_conversation_id=target_conversation_id,
                    original_document=original_document,
                    object_key=target_key,
                )

                attachment_id_mapping[old_file_id] = new_file_id

                cloned_attachment = attachment.copy()
                cloned_attachment["id"] = new_file_id
                cloned_attachments.append(cloned_attachment)

            except Exception as e:
                logger.error(f"Failed to clone attachment {old_file_id}: {str(e)}")
                continue

        logger.info(f"Successfully cloned {len(cloned_attachments)} out of {len(attachments)} attachments")
        return cloned_attachments

    def clone_vector_db_entries(
        self,
        source_conversation_id: str,
        target_conversation_id: str,
        attachment_id_mapping: dict[str, str],
        chatbot_id: str,
    ) -> None:
        """Clone vector database entries for cloned attachments.

        Args:
            source_conversation_id (str): The ID of the source conversation containing the original attachments.
            target_conversation_id (str): The ID of the target conversation where attachments will be cloned.
            attachment_id_mapping (dict[str, str]): Mapping of old file IDs to new file IDs to track cloned files.
            chatbot_id (str): The ID of the chatbot to get pipeline configuration for vector DB cloning.

        Returns:
            None
        """
        try:
            # Get pipeline configuration
            pipeline_manager = PluginManager()
            pipeline_handler = pipeline_manager.get_handler(PipelineHandler)
            pipeline_config = pipeline_handler.get_pipeline_config(chatbot_id)

            # Get vector database instance and clone entries
            from claudia_gpt.component.vector_db.vector_db_factory import VectorDBFactory

            vector_db = VectorDBFactory().get_vector_db(pipeline_config=pipeline_config)
            vector_db.clone_vector_entries(
                source_conversation_id=source_conversation_id,
                target_conversation_id=target_conversation_id,
                attachment_id_mapping=attachment_id_mapping,
            )

        except Exception as e:
            logger.error(f"Failed to clone vector DB entries: {str(e)}")

    def setup_shared_conversation_continuation(
        self,
        shared_conversation: SharedConversation,
        chatbot_id: str,
        new_user_id: str,
        new_conversation_id: str | None = None,
        anonymizer_storage: AnonymizerStorage | None = None,
    ) -> SharedConversationSetupResult:
        """Set up a new conversation based on a shared conversation.

        Args:
            shared_conversation (SharedConversation): The shared conversation.
            chatbot_id (str): The chatbot ID.
            new_user_id (str): The user ID of the new conversation.
            new_conversation_id (str | None): The ID of the new conversation.
                                              If None, a new conversation will be created.
            anonymizer_storage (AnonymizerStorage | None): The anonymizer storage instance.

        Returns:
            SharedConversationSetupResult: The result of setting up the shared conversation continuation.
        """
        if not new_conversation_id:
            new_conversation_id = self._create_target_conversation(new_user_id, shared_conversation, chatbot_id)

        original_messages = self.chat_history_storage.get_messages(
            user_id=shared_conversation.user_id,
            conversation_id=shared_conversation.conversation_id,
            max_timestamp=shared_conversation.last_updated_time,
        )

        cloned_messages = self._clone_conversation_content(
            shared_conversation, new_user_id, new_conversation_id, chatbot_id, original_messages, anonymizer_storage
        )

        original_message_ids = [msg.id for msg in original_messages]
        cloned_message_ids = [msg.id for msg in cloned_messages]

        message_id_mapping = self._create_message_id_mapping(original_message_ids, cloned_message_ids)

        return SharedConversationSetupResult(
            new_conversation_id=new_conversation_id,
            cloned_messages=cloned_messages,
            chatbot_id=chatbot_id,
            message_id_mapping=message_id_mapping,
        )

    def validate_and_get_shared_conversation(self, shared_conversation_id: str) -> tuple[SharedConversation, str]:
        """Validate shared conversation and get chatbot ID.

        Args:
            shared_conversation_id (str): The shared conversation ID.

        Returns:
            tuple[SharedConversation, str]: Shared conversation and chatbot ID
        """
        shared_conversation = self.get_shared_conversation(shared_conversation_id)

        original_conversation = self.chat_history_storage.get_conversation(
            shared_conversation.user_id, shared_conversation.conversation_id
        )
        if not original_conversation:
            logger.info(
                f"Original conversation {shared_conversation.conversation_id} linked to "
                f"shared conversation {shared_conversation_id} was not found."
            )
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Original conversation not found")

        return shared_conversation, original_conversation.chatbot_id

    def _create_target_conversation(
        self, new_user_id: str, shared_conversation: SharedConversation, chatbot_id: str
    ) -> str:
        """Create the target conversation for continuation.

        Args:
            new_user_id (str): The user ID of the new conversation.
            shared_conversation (SharedConversation): The shared conversation.
            chatbot_id (str): The chatbot ID.

        Returns:
            str: The ID of the new conversation.
        """
        original_conversation = self.chat_history_storage.get_conversation(
            shared_conversation.user_id, shared_conversation.conversation_id
        )

        new_conversation = self.chat_history_storage.create_conversation(
            user_id=new_user_id,
            conversation_title=(original_conversation.title or "Shared Conversation") + " (cont.)",
            chatbot_id=chatbot_id,
        )

        logger.info(
            f"Created new conversation {new_conversation.id} for user {new_user_id} "
            f"continuing from shared conversation {shared_conversation.id}"
        )

        return new_conversation.id

    def _clone_conversation_content(  # noqa: PLR0913
        self,
        shared_conversation: SharedConversation,
        new_user_id: str,
        new_conversation_id: str,
        chatbot_id: str,
        original_messages: list["Message"],
        anonymizer_storage: AnonymizerStorage | None = None,
    ) -> list["Message"]:
        """Clone messages and attachments from shared conversation.

        Args:
            shared_conversation (SharedConversation): The shared conversation.
            new_user_id (str): The user ID of the new conversation.
            new_conversation_id (str): The ID of the new conversation.
            chatbot_id (str): The chatbot ID.
            original_messages (list[Message]): The original messages.
            anonymizer_storage (AnonymizerStorage | None): The anonymizer storage instance.

        Returns:
            list[Message]: The cloned messages.
        """
        # Extract only the attachment data we need
        message_attachments = self._extract_message_attachments(original_messages)

        # Clone attachments
        attachment_id_mapping, cloned_attachments_metadata = self._clone_all_attachments(
            message_attachments, shared_conversation.conversation_id, new_conversation_id
        )

        # Clone PII mappings if anonymizer storage is available
        if anonymizer_storage:
            self.clone_pii_mappings(
                source_conversation_id=shared_conversation.conversation_id,
                target_conversation_id=new_conversation_id,
                anonymizer_storage=anonymizer_storage,
            )

        # Clone messages
        cloned_messages: list["Message"] = self.clone_messages_to_conversation(
            source_user_id=shared_conversation.user_id,
            source_conversation_id=shared_conversation.conversation_id,
            target_user_id=new_user_id,
            target_conversation_id=new_conversation_id,
            max_timestamp=shared_conversation.last_updated_time,
            cloned_attachments_metadata=cloned_attachments_metadata,
        )

        # Clone vector database entries
        if attachment_id_mapping:
            self.clone_vector_db_entries(
                source_conversation_id=shared_conversation.conversation_id,
                target_conversation_id=new_conversation_id,
                attachment_id_mapping=attachment_id_mapping,
                chatbot_id=chatbot_id,
            )

        logger.info(
            f"Cloned {len(cloned_messages)//2} AI-User message pairs from shared conversation "
            f"{shared_conversation.id} to new conversation {new_conversation_id}"
        )

        return cloned_messages

    def _extract_message_attachments(self, messages: list["Message"]) -> dict[str, list[dict[str, Any]]]:
        """Extract attachment metadata from messages.

        Args:
            messages (list[Message]): The messages to extract attachments from.

        Returns:
            dict[str, list[dict[str, Any]]]: Mapping of message ID to attachment list.
        """
        message_attachments: dict[str, list[dict[str, Any]]] = {}
        for message in messages:
            if message.metadata_ and message.metadata_.get("attachments"):
                message_attachments[message.id] = message.metadata_["attachments"]
        return message_attachments

    def _clone_all_attachments(
        self,
        message_attachments: dict[str, list[dict[str, Any]]],
        source_conversation_id: str,
        target_conversation_id: str,
    ) -> tuple[dict[str, str], dict[str, Any]]:
        """Clone attachments for messages that have them.

        Args:
            message_attachments (dict[str, list[dict[str, Any]]]): Mapping of message ID to attachments.
            source_conversation_id (str): The ID of the source conversation.
            target_conversation_id (str): The ID of the target conversation.

        Returns:
            tuple[dict[str, str], dict[str, Any]]: The attachment ID mapping and cloned attachments metadata.
        """
        attachment_id_mapping: dict[str, str] = {}
        cloned_attachments_metadata: dict[str, Any] = {}

        for message_id, attachments in message_attachments.items():
            cloned_attachments = self.clone_message_attachments(
                source_conversation_id=source_conversation_id,
                target_conversation_id=target_conversation_id,
                attachments=attachments,
                attachment_id_mapping=attachment_id_mapping,
            )
            if cloned_attachments:
                cloned_attachments_metadata[message_id] = cloned_attachments

        return attachment_id_mapping, cloned_attachments_metadata

    def _create_message_id_mapping(
        self,
        original_message_ids: list[str],
        cloned_message_ids: list[str],
    ) -> dict[str, str]:
        """Create mapping from original message IDs to cloned message IDs.

        Args:
            original_message_ids (list[str]): The original message IDs.
            cloned_message_ids (list[str]): The cloned message IDs.

        Returns:
            dict[str, str]: The mapping from original message IDs to cloned message IDs.
        """
        if len(original_message_ids) != len(cloned_message_ids):
            logger.warning(
                f"Mismatch in message count: {len(original_message_ids)} original vs {len(cloned_message_ids)} cloned"
            )

        return dict(zip(original_message_ids, cloned_message_ids))

    def clone_messages_to_conversation(  # noqa: PLR0913
        self,
        source_user_id: str,
        source_conversation_id: str,
        target_user_id: str,
        target_conversation_id: str,
        max_timestamp: datetime,
        cloned_attachments_metadata: dict[str, Any] | None = None,
    ) -> list["Message"]:
        """Clone messages from source conversation to target conversation up to max_timestamp.

        Args:
            source_user_id: Original conversation owner
            source_conversation_id: Original conversation ID
            target_user_id: New conversation owner
            target_conversation_id: New conversation ID
            max_timestamp: Only clone messages created before this time
            cloned_attachments_metadata: Pre-cloned attachment metadata from helper layer

        Returns:
            List of cloned messages
        """
        # Setup cloning context
        source_messages, id_mapping = self._prepare_cloning_context(
            source_user_id, source_conversation_id, target_conversation_id, max_timestamp
        )

        # Clone each message
        cloned_messages: list["Message"] = []
        for message in source_messages:
            cloned_message = self._clone_single_message(
                message=message,
                target_user_id=target_user_id,
                target_conversation_id=target_conversation_id,
                id_mapping=id_mapping,
                cloned_attachments_metadata=cloned_attachments_metadata,
            )
            cloned_messages.append(cloned_message)

        return cloned_messages

    def _prepare_cloning_context(
        self,
        source_user_id: str,
        source_conversation_id: str,
        target_conversation_id: str,
        max_timestamp: datetime,
    ) -> tuple[list["Message"], dict[str, str]]:
        """Prepare the context for message cloning.

        Args:
            source_user_id: Original conversation owner
            source_conversation_id: Original conversation ID
            target_conversation_id: New conversation ID
            max_timestamp: Only get messages created before this time

        Returns:
            Tuple of (source_messages, id_mapping)
        """
        # Get messages from source conversation
        source_messages = self.chat_history_storage.get_messages(
            user_id=source_user_id, conversation_id=source_conversation_id, max_timestamp=max_timestamp
        )

        # Initialize ID mapping with conversation ID
        id_mapping: dict[str, str] = {source_conversation_id: target_conversation_id}

        return source_messages, id_mapping

    def _clone_single_message(
        self,
        message: "Message",
        target_user_id: str,
        target_conversation_id: str,
        id_mapping: dict[str, str],
        cloned_attachments_metadata: dict[str, Any] | None = None,
    ) -> "Message":
        """Clone a single message with proper ID mapping and metadata.

        Args:
            message: Original message to clone
            target_user_id: New conversation owner
            target_conversation_id: New conversation ID
            id_mapping: Mapping of old IDs to new IDs (updated in place)
            cloned_attachments_metadata: Pre-cloned attachment metadata

        Returns:
            Message: Cloned message
        """
        new_message_id = str(uuid4())
        logger.info(f"Cloning message: source_id={message.id}, new_id={new_message_id}")

        # Determine correct parent ID
        new_parent_id = self._determine_new_parent_id(
            original_parent_id=message.parent_id,
            id_mapping=id_mapping,
            fallback_parent_id=target_conversation_id,
        )

        # Prepare metadata
        cloned_metadata = message.metadata_.copy() if message.metadata_ else {}
        if cloned_attachments_metadata and message.id in cloned_attachments_metadata:
            cloned_metadata["attachments"] = cloned_attachments_metadata[message.id]
        cloned_metadata[ChatHistoryConstants.IS_FROM_SHARED_CONVERSATION_KEY] = True

        # Create the cloned message
        cloned_message = self.chat_history_storage.add_message(
            message_role=message.role,
            message=message.content,
            user_id=target_user_id,
            conversation_id=target_conversation_id,
            parent_id=new_parent_id,
            source=message.source or "shared_conversation_clone",
            metadata_=cloned_metadata,
            id=new_message_id,
        )

        # Update ID mapping for future references
        if message.id and message.id.strip():
            id_mapping[message.id] = new_message_id

        logger.info(f"Successfully cloned message {message.id} -> {new_message_id}")
        return cloned_message

    def _determine_new_parent_id(
        self,
        original_parent_id: str | None,
        id_mapping: dict[str, str],
        fallback_parent_id: str,
    ) -> str:
        """Determine the correct parent ID for a cloned message.

        Args:
            original_parent_id: The original message's parent ID
            id_mapping: Mapping of old IDs to new IDs
            fallback_parent_id: Fallback parent ID (usually conversation ID)

        Returns:
            The new parent ID to use
        """
        if original_parent_id and original_parent_id.strip():
            mapped_parent = id_mapping.get(original_parent_id)
            if mapped_parent:
                logger.info(f"Mapped parent_id {original_parent_id} -> {mapped_parent}")
                return mapped_parent

        logger.info(f"Using fallback parent_id: {fallback_parent_id}")
        return fallback_parent_id

    def clone_pii_mappings(
        self,
        source_conversation_id: str,
        target_conversation_id: str,
        anonymizer_storage: AnonymizerStorage,
    ) -> None:
        """Clone PII mappings from source to target conversation.

        Args:
            source_conversation_id (str): The source conversation ID.
            target_conversation_id (str): The target conversation ID.
            anonymizer_storage (AnonymizerStorage): The anonymizer storage instance.
        """
        try:
            anonymizer_storage.clone_mappings_to_conversation(
                source_conversation_id=source_conversation_id, target_conversation_id=target_conversation_id
            )
            logger.info(f"Successfully cloned PII mappings from {source_conversation_id} to {target_conversation_id}")
        except Exception as e:
            logger.error(f"Failed to clone PII mappings: {str(e)}")
            # Don't raise the exception to avoid breaking the conversation cloning process
