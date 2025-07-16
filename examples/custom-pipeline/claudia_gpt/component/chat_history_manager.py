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

from claudia_gpt.anonymizer.anonymizer_storage import AnonymizerStorage
from claudia_gpt.anonymizer.schemas import AnonymizerMapping
from claudia_gpt.api.model.reference import ReferenceMetadata
from claudia_gpt.chat_history import ChatHistoryStorage
from claudia_gpt.chat_history.schemas import Message, MessageRole


class ChatHistoryManager(Component):
    """Manage the conversation history.

    Attributes:
        OP_READ (str): The operation to retrieve the conversation history.
        OP_WRITE (str): The operation to save the conversation history.
        IS_MULTIMODAL_KEY (str): The key for the is multimodal flag.
        NEW_ANONYMIZED_MAPPINGS_KEY (str): The key for the new anonymized mappings.
        storage (ChatHistoryStorage | None): The chat history storage.
        MEDIA_MAPPING_KEY (str): The key for the media mapping.
        RESPONSE_KEY (str): The key for the responses.
        QUERY_KEY (str): The key for the query.
        TRANSFORMED_QUERY_KEY (str): The key for the transformed query.
        CHAT_HISTORY_KEY (str): The key for the chat history.
        USER_ID_KEY (str): The key for the user ID.
        CONVERSATION_ID_KEY (str): The key for the conversation ID.
        SOURCE_KEY (str): The key for the source.
        ATTACHMENTS_KEY (str): The key for the attachments.
        ASSISTANT_MESSAGE_ID_KEY (str): The key for the assistant message ID.
        USER_MESSAGE_ID_KEY (str): The key for the user message ID.
        PARENT_ID_KEY (str): The key for the parent ID.
        LIMIT_KEY (str): The key for the limit.
        REFERENCES_KEY (str): The key for the references.
        RELATED_KEY (str): The key for the related questions.
        SEARCH_TYPE_KEY (str): The key for the search type.
        ANONYMIZE_EM_KEY (str): The key for the anonymize EM.
        ANONYMIZE_LM_KEY (str): The key for the anonymize LM.
        STEP_INDICATORS_KEY (str): The key for the step indicators.
        STEPS_KEY (str): The key for the steps.
        AGENT_IDS_KEY (str): The key for the agent IDs.
        EVENT_EMITTER_KEY (str): The key for the event emitter.
        OPERATION_KEY (str): The key for the operation.
        AGENT_TYPE_KEY (str): The key for the agent type.
        CONTEXT_KEY (str): The key for the context.
        storage (ChatHistoryStorage | None): The chat history storage.
    """

    OP_READ = "retrieve"
    OP_WRITE = "save"
    IS_MULTIMODAL_KEY = "is_multimodal"
    NEW_ANONYMIZED_MAPPINGS_KEY = "new_anonymized_mappings"
    MEDIA_MAPPING_KEY = "media_mapping"
    RESPONSE_KEY = "response"
    QUERY_KEY = "query"
    TRANSFORMED_QUERY_KEY = "transformed_query"
    CHAT_HISTORY_KEY = "chat_history"
    USER_ID_KEY = "user_id"
    CONVERSATION_ID_KEY = "conversation_id"
    SOURCE_KEY = "source"
    ATTACHMENTS_KEY = "attachments"
    ASSISTANT_MESSAGE_ID_KEY = "assistant_message_id"
    USER_MESSAGE_ID_KEY = "user_message_id"
    PARENT_ID_KEY = "parent_id"
    LIMIT_KEY = "limit"
    REFERENCES_KEY = "references"
    RELATED_KEY = "related"
    SEARCH_TYPE_KEY = "search_type"
    ANONYMIZE_EM_KEY = "anonymize_em"
    ANONYMIZE_LM_KEY = "anonymize_lm"
    STEP_INDICATORS_KEY = "step_indicators"
    STEPS_KEY = "steps"
    AGENT_IDS_KEY = "agent_ids"
    EVENT_EMITTER_KEY = "event_emitter"
    OPERATION_KEY = "operation"
    AGENT_TYPE_KEY = "agent_type"
    CONTEXT_KEY = "context"
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
        self.storage = storage
        self.anonymizer_storage = anonymizer_storage
        self._streamable = True

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
                and conversation ID.

        Returns:
            list[tuple[PromptRole, str | list[Any]]] | None: The formatted chat history,
                or None if the chat history is disabled.
        """
        chat_history = kwargs.get(self.CHAT_HISTORY_KEY)
        user_id = kwargs.get(self.USER_ID_KEY)
        conversation_id = kwargs.get(self.CONVERSATION_ID_KEY)
        limit = kwargs.get(self.LIMIT_KEY)
        is_multimodal = kwargs.get(self.IS_MULTIMODAL_KEY, False)

        if not chat_history and self.storage and conversation_id and user_id:
            chat_history = self.storage.get_messages(user_id, conversation_id, limit)

        return self._format_chat_history(chat_history, is_multimodal)

    # Custom implementation for Claudia
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
        media_mapping = kwargs.get(self.MEDIA_MAPPING_KEY)

        user_metadata: dict[str, Any] = {}
        ai_metadata: dict[str, Any] = {}

        agent_type = kwargs.get(self.AGENT_TYPE_KEY)
        context = kwargs.get(self.CONTEXT_KEY)

        if attachments:
            user_metadata.update(attachments)

        anonymize_metadata_keys = [self.ANONYMIZE_EM_KEY, self.ANONYMIZE_LM_KEY]
        anonymize_metadata_metadata = {
            key: value for key in anonymize_metadata_keys if (value := kwargs.get(key)) is not None
        }
        user_metadata.update(anonymize_metadata_metadata)
        ai_metadata.update(anonymize_metadata_metadata)

        user_metadata_keys = [self.SEARCH_TYPE_KEY, self.AGENT_IDS_KEY]
        user_metadata.update({key: value for key in user_metadata_keys if (value := kwargs.get(key))})

        ai_metadata_keys = [
            self.RELATED_KEY,
            self.SEARCH_TYPE_KEY,
            self.STEP_INDICATORS_KEY,
            self.STEPS_KEY,
            self.AGENT_IDS_KEY,
            self.MEDIA_MAPPING_KEY,
            self.TRANSFORMED_QUERY_KEY,
        ]
        ai_metadata.update({key: value for key in ai_metadata_keys if (value := kwargs.get(key))})

        if references:
            reference_metadata = self._create_reference_metadata(references)
            if reference_metadata:
                ai_metadata.update({self.REFERENCES_KEY: reference_metadata})

        user_message = self.storage.add_user_message(
            message=query,
            user_id=user_id,
            conversation_id=conversation_id,
            parent_id=parent_id,
            source=MessageRole.USER.value,
            metadata_=user_metadata,
            id=user_message_id,
            agent_type=agent_type,
        )
        ai_message = self.storage.add_ai_message(
            message=response,
            user_id=user_id,
            conversation_id=conversation_id,
            parent_id=user_message.id,
            source=source,
            metadata_=ai_metadata,
            id=assistant_message_id,
            agent_type=agent_type,
            context=context,
        )

        self._store_new_anonymized_mappings(kwargs.get(self.NEW_ANONYMIZED_MAPPINGS_KEY, []))

        if not event_emitter:
            return

        if media_mapping:
            await event_emitter.emit(
                value=json.dumps(
                    {
                        "data_type": "media_mapping",
                        "data_value": media_mapping,
                    }
                ),
                event_level=EventLevel.INFO,
                event_type=EventType.DATA,
            )

        mappings = (
            self.anonymizer_storage.get_mappings_by_conversation_id(conversation_id) if self.anonymizer_storage else []
        )
        deanonymized_mapping = {mapping.anonymized_value: mapping.pii_value for mapping in mappings}

        deanonymize_messages = self.storage.get_deanonymized_messages(
            messages=[user_message, ai_message],
            is_anonymized=True,
            mappings=mappings,
        )

        await event_emitter.emit(
            value=json.dumps(
                {
                    "data_type": "deanonymized_data",
                    "data_value": {
                        "user_message": {
                            "content": deanonymize_messages[0].content,
                            "deanonymized_content": deanonymize_messages[0].deanonymized_content,
                        },
                        "ai_message": {
                            "content": deanonymize_messages[1].content,
                            "deanonymized_content": deanonymize_messages[1].deanonymized_content,
                        },
                        "deanonymized_mapping": deanonymized_mapping,
                    },
                }
            ),
            event_level=EventLevel.INFO,
            event_type=EventType.DATA,
        )

    def _format_chat_history(
        self, messages: list[Message | dict[str, Any]], is_multimodal: bool
    ) -> list[tuple[PromptRole, str | list[Any]]] | None:
        """Format the chat history.

        Args:
            messages (list[Message | dict[str, Any]]): The list of messages from storage or frontend application.
            is_multimodal (bool): Whether the chat history is multimodal.

        Returns:
            list[tuple[PromptRole, str | list[Any]]] | None: The formatted chat history.
        """
        if not messages:
            return None

        message_dict = [message.model_dump() if isinstance(message, Message) else message for message in messages]

        if is_multimodal:
            return [(PromptRole(message["role"]), [message["content"]]) for message in message_dict]

        return [(PromptRole(message["role"]), message["content"]) for message in message_dict]

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
