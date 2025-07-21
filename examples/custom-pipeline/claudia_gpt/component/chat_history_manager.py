"""Manage the conversation history.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Hermes Vincentius Gani (hermes.v.gani@gdplabs.id)

References:
    None
"""

import json
from typing import Any

from gllm_core.constants import EventLevel, EventType
from gllm_core.schema import Component
from gllm_core.schema.chunk import Chunk
from gllm_inference.schema import PromptRole
from gllm_misc.chat_history_manager import ChatHistoryManager as SDKChatHistoryManager

from claudia_gpt.anonymizer.anonymizer_storage import (
    AnonymizerStorage,
)
from claudia_gpt.anonymizer.schemas import AnonymizerMapping
from claudia_gpt.api.helper.message.constants import (
    QUOTE_HISTORY_FORMAT,
    QUOTE_REPLY_FORMAT,
    PipelineEventKeys,
)
from claudia_gpt.api.model.reference import ReferenceMetadata
from claudia_gpt.chat_history import ChatHistoryStorage
from claudia_gpt.chat_history.constants import ChatHistoryConstants
from claudia_gpt.chat_history.schemas import (
    Message,
)


class ChatHistoryManager(Component, ChatHistoryConstants):
    """Manage the conversation history.

    See the ChatHistoryConstants class for the constants.

    Attributes:
        storage (ChatHistoryStorage | None): The chat history storage.
    """

    storage: ChatHistoryStorage | None = None

    def __init__(
        self,
        storage: ChatHistoryStorage | None = None,
        anonymizer_storage: AnonymizerStorage | None = None,
    ):
        """Initialize the ChatHistoryManager class.

        Args:
            storage (ChatHistoryStorage | None): The chat history storage.
            anonymizer_storage (AnonymizerStorage | None): The anonymizer storage.
        """
        from claudia_gpt.utils.initializer import (
            get_sdk_chat_history_manager,
        )  # fix circular import

        self.storage = storage
        self.anonymizer_storage = anonymizer_storage
        self._streamable = True
        self.sdk_chat_history_manager: SDKChatHistoryManager = get_sdk_chat_history_manager()

    async def _run(self, **kwargs: str) -> Any:
        """Run the chat history manager component.

        Args:
            kwargs (Any): The keyword arguments, which may contain the operation.

        Returns:
            Any: The result of the operation.
        """
        if not self.storage:
            return None

        operation = kwargs.get(self.OPERATION_KEY)

        if operation == self.OP_READ:
            return await self.read(kwargs)

        if operation == self.OP_WRITE:
            return await self.write(kwargs)

    async def read(self, kwargs: Any) -> list[tuple[PromptRole, str | list[Any]]] | None:
        """Retrieve the conversation history.

        It will use the chat history from the frontend application if it is available.
        Otherwise, it will retrieve the chat history from the storage.

        Args:
            kwargs (Any): The keyword arguments, which may contain the chat history, user ID,
                limit, last message ID, and conversation ID.

        Returns:
            list[tuple[PromptRole, str | list[Any]]] | None: The formatted chat history,
                or None if the chat history is disabled.
        """
        chat_history = kwargs.get(self.CHAT_HISTORY_KEY)
        conversation_id = kwargs.get(self.CONVERSATION_ID_KEY)
        limit = kwargs.get(self.LIMIT_KEY)
        last_message_id = kwargs.get(self.LAST_MESSAGE_ID_KEY)

        if not chat_history and self.storage and conversation_id:
            chat_history = await self.sdk_chat_history_manager.retrieve(
                conversation_id=conversation_id,
                pair_limit=limit,
                last_message_id=last_message_id,
            )

        return chat_history

    async def write(self, kwargs: Any) -> None:
        """Save the conversation history.

        Args:
            kwargs (Any): The keyword arguments, which may contain the user ID, conversation ID,
                        query, response, references, parent ID, user message ID, assistant message ID,
                        and source.
        """
        user_id = kwargs.get(self.USER_ID_KEY)
        conversation_id = kwargs.get(self.CONVERSATION_ID_KEY)

        if not self.storage or not user_id or not conversation_id:
            return None

        query = kwargs.get(self.QUERY_KEY)
        response = kwargs.get(self.RESPONSE_KEY)
        references = kwargs.get(self.REFERENCES_KEY)
        parent_id = kwargs.get(self.PARENT_ID_KEY)
        user_message_id = kwargs.get(self.USER_MESSAGE_ID_KEY)
        assistant_message_id = kwargs.get(self.ASSISTANT_MESSAGE_ID_KEY)
        attachments = kwargs.get(self.ATTACHMENTS_KEY)
        source = kwargs.get(self.SOURCE_KEY)
        event_emitter = kwargs.get(self.EVENT_EMITTER_KEY)
        quote = kwargs.get(self.QUOTE_KEY)

        user_metadata: dict[str, Any] = {}
        assistant_metadata: dict[str, Any] = {}

        if attachments:
            user_metadata.update(attachments)

        if quote:
            user_metadata[self.QUOTE_KEY] = quote
            query = kwargs.get(self.ORIGINAL_MESSAGE_KEY)

        anonymize_metadata_keys = [self.ANONYMIZE_EM_KEY, self.ANONYMIZE_LM_KEY]
        anonymize_metadata_metadata = {
            key: value for key in anonymize_metadata_keys if (value := kwargs.get(key)) is not None
        }
        user_metadata.update(anonymize_metadata_metadata)
        assistant_metadata.update(anonymize_metadata_metadata)

        user_metadata_keys = [self.SEARCH_TYPE_KEY, self.AGENT_IDS_KEY]
        user_metadata.update({key: value for key in user_metadata_keys if (value := kwargs.get(key))})

        assistant_metadata_keys = [
            self.RELATED_KEY,
            self.SEARCH_TYPE_KEY,
            self.STEP_INDICATORS_KEY,
            self.STEPS_KEY,
            self.AGENT_IDS_KEY,
            self.MEDIA_MAPPING_KEY,
            self.CACHE_HIT_KEY,
        ]
        assistant_metadata.update({key: value for key in assistant_metadata_keys if (value := kwargs.get(key))})

        if references:
            reference_metadata = self._create_reference_metadata(references)
            if reference_metadata:
                assistant_metadata.update({self.REFERENCES_KEY: reference_metadata})

        await self.sdk_chat_history_manager.store(
            user_message_id=user_message_id,
            assistant_message_id=assistant_message_id,
            conversation_id=conversation_id,
            user_message=query,
            assistant_message=response,
            parent_id=parent_id,
            is_active=True,
            source=source,
            user_metadata=user_metadata,
            assistant_metadata=assistant_metadata,
        )

        if quote:
            query = QUOTE_REPLY_FORMAT.format(quote=quote, query=query)

        self._store_new_anonymized_mappings(kwargs.get(self.NEW_ANONYMIZED_MAPPINGS_KEY, []))

        if not event_emitter:
            return

        mappings = (
            self.anonymizer_storage.get_mappings_by_conversation_id(conversation_id) if self.anonymizer_storage else []
        )
        deanonymized_mapping = {mapping.anonymized_value: mapping.pii_value for mapping in mappings}

        deanonymize_message_contents = self.storage.get_deanonymized_texts(
            texts=[query, response],
            is_anonymized=True,
            mappings=mappings,
        )

        await event_emitter.emit(
            value=json.dumps(
                {
                    "data_type": PipelineEventKeys.DEANONYMIZED_DATA,
                    "data_value": {
                        "user_message": {
                            "content": query,
                            "deanonymized_content": deanonymize_message_contents[0],
                        },
                        "ai_message": {
                            "content": response,
                            "deanonymized_content": deanonymize_message_contents[1],
                        },
                        "deanonymized_mapping": deanonymized_mapping,
                    },
                }
            ),
            event_level=EventLevel.INFO,
            event_type=EventType.DATA,
        )

    def _format_chat_history(
        self, messages: list[Message | dict[str, Any]], is_multimodal: bool, last_message_id: str | None
    ) -> list[tuple[PromptRole, str | list[Any]]] | None:
        """Format the chat history.

        Args:
            messages (list[Message | dict[str, Any]]): The list of messages from storage or frontend application.
            is_multimodal (bool): Whether the chat history is multimodal.
            last_message_id (str | None): The last message ID for traversal, or None for original behavior.

        Returns:
            list[tuple[PromptRole, str | list[Any]]] | None: The formatted chat history.
        """
        if not messages:
            return None

        message_dicts: list[dict[str, Any]] = [
            message.model_dump() if isinstance(message, Message) else message for message in messages
        ]

        if last_message_id:
            return self._format_chat_history_with_traversal(message_dicts, is_multimodal, last_message_id)
        else:
            return self._format_chat_history_all_messages(message_dicts, is_multimodal)

    def _format_chat_history_all_messages(
        self, message_dicts: list[dict[str, Any]], is_multimodal: bool
    ) -> list[tuple[PromptRole, str | list[Any]]]:
        """Format all messages without traversal (original behavior).

        Args:
            message_dicts (list[dict[str, Any]]): List of message dictionaries.
            is_multimodal (bool): Whether the chat history is multimodal.

        Returns:
            list[tuple[PromptRole, str | list[Any]]]: The formatted chat history.
        """
        # Apply quote formatting
        for message in message_dicts:
            metadata: dict[str, Any] = message.get("metadata_", {})
            if metadata and metadata.get("quote", ""):
                message["content"] = QUOTE_HISTORY_FORMAT.format(quote=metadata.get("quote"), query=message["content"])

        return (
            [(PromptRole(msg["role"]), [msg["content"]]) for msg in message_dicts]
            if is_multimodal
            else [(PromptRole(msg["role"]), msg["content"]) for msg in message_dicts]
        )

    def _format_chat_history_with_traversal(
        self, message_dicts: list[dict[str, Any]], is_multimodal: bool, last_message_id: str
    ) -> list[tuple[PromptRole, str | list[Any]]] | None:
        """Format chat history using message traversal from last_message_id.

        Args:
            message_dicts (list[dict[str, Any]]): List of message dictionaries.
            is_multimodal (bool): Whether the chat history is multimodal.
            last_message_id (str): The last message ID to start traversal from.

        Returns:
            list[tuple[PromptRole, str | list[Any]]] | None: The formatted chat history or None if traversal fails.
        """
        message_lookup: dict[str, dict[str, Any]] = {msg["id"]: msg for msg in message_dicts if msg.get("id")}

        if last_message_id not in message_lookup:
            return None

        conversation_id: str | None = message_lookup[last_message_id].get("conversation_id")
        if not conversation_id:
            return None
        formatted_messages: list[tuple[PromptRole, str | list[Any]]] = []
        current_message_id: str = last_message_id

        while current_message_id in message_lookup:
            current_message = message_lookup[current_message_id]

            # Apply quote formatting
            content: str = current_message["content"]
            metadata: dict[str, Any] = current_message.get("metadata_", {})
            if metadata and metadata.get("quote", ""):
                content = QUOTE_HISTORY_FORMAT.format(quote=metadata.get("quote"), query=content)

            role = PromptRole(current_message["role"])
            formatted_messages.append((role, [content] if is_multimodal else content))

            parent_id = current_message.get("parent_id")

            # Stop when we reach the conversation root
            if parent_id == conversation_id or not parent_id:
                break

            current_message_id = parent_id

        # Return in chronological order (oldest first)
        return formatted_messages[::-1]

    def _store_new_anonymized_mappings(self, new_anonymized_mappings: list[AnonymizerMapping]) -> None:
        """Store new anonymized mappings in the anonymizer storage.

        This function iterates over a list of `AnonymizerMapping` objects and stores each mapping in the
        anonymizer storage if the storage is available. Each mapping represents a record linking
        anonymized values to their original Personally Identifiable Information (PII).

        Args:
            new_anonymized_mappings (list[AnonymizerMapping]): List of `AnonymizerMapping` objects containing
                conversation IDs, PII types, anonymized values, and original PII values.
        """
        if self.anonymizer_storage:
            for mapping in new_anonymized_mappings:
                self.anonymizer_storage.create_mapping(
                    mapping.conversation_id,
                    mapping.pii_type,
                    mapping.anonymized_value,
                    mapping.pii_value,
                )

    def _create_reference_metadata(self, references: list[Chunk]) -> list[dict[str, Any]]:
        """Create reference metadata for references.

        Args:
            references (list[Chunk]): The list of references.

        Returns:
            list[dict[str, Any]]: The list of reference metadata.
        """
        reference_metadata: list[dict[str, Any]] = []

        for reference in references:
            metadata = getattr(reference, "metadata", {})
            metadata["content"] = getattr(reference, "content", "")
            filtered_metadata = ReferenceMetadata(**metadata)
            reference_metadata.append(filtered_metadata.model_dump(exclude_none=True))

        return reference_metadata
