"""Constants for chat history module.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""


class ChatHistoryConstants:
    """Constants for chat history module.

    Attributes:
        STEP_INDICATORS_KEY (str): The key for the step indicators.
        STEPS_KEY (str): The key for the steps.
        REFERENCES_KEY (str): The key for the references.
        RELATED_KEY (str): The key for the related.
        ATTACHMENTS_KEY (str): The key for the attachments.
        QUOTE_KEY (str): The key for the quote.
        SEARCH_TYPE_KEY (str): The key for the search type.
        ANONYMIZE_EM_KEY (str): The key for the anonymize EM.
        ANONYMIZE_LM_KEY (str): The key for the anonymize LM.
        MEDIA_MAPPING_KEY (str): The key for the media mapping.
        USER_ID_KEY (str): The key for the user ID.
        CONVERSATION_ID_KEY (str): The key for the conversation ID.
        SOURCE_KEY (str): The key for the source.
        ASSISTANT_MESSAGE_ID_KEY (str): The key for the assistant message ID.
        USER_MESSAGE_ID_KEY (str): The key for the user message ID.
        PARENT_ID_KEY (str): The key for the parent ID.
        LIMIT_KEY (str): The key for the limit.
        AGENT_IDS_KEY (str): The key for the agent IDs.
        EVENT_EMITTER_KEY (str): The key for the event emitter.
        OP_READ (str): The key for the read operation.
        OP_WRITE (str): The key for the write operation.
        IS_MULTIMODAL_KEY (str): The key for the is multimodal.
        NEW_ANONYMIZED_MAPPINGS_KEY (str): The key for the new anonymized mappings.
        RESPONSE_KEY (str): The key for the response.
        QUERY_KEY (str): The key for the query.
        ORIGINAL_MESSAGE_KEY (str): The key for the original message.
        CHAT_HISTORY_KEY (str): The key for the chat history.
        OPERATION_KEY (str): The key for the operation.
        LAST_MESSAGE_ID_KEY (str): The key for the last message ID.
        CACHE_HIT_KEY (str): The key for the cache hit flag.
    """

    # Chat history metadata keys
    STEP_INDICATORS_KEY = "step_indicators"
    STEPS_KEY = "steps"
    REFERENCES_KEY = "references"
    RELATED_KEY = "related"
    ATTACHMENTS_KEY = "attachments"
    QUOTE_KEY = "quote"
    SEARCH_TYPE_KEY = "search_type"
    ANONYMIZE_EM_KEY = "anonymize_em"
    ANONYMIZE_LM_KEY = "anonymize_lm"
    MEDIA_MAPPING_KEY = "media_mapping"
    USER_ID_KEY = "user_id"
    CONVERSATION_ID_KEY = "conversation_id"
    SOURCE_KEY = "source"
    ASSISTANT_MESSAGE_ID_KEY = "assistant_message_id"
    USER_MESSAGE_ID_KEY = "user_message_id"
    PARENT_ID_KEY = "parent_id"
    LIMIT_KEY = "limit"
    AGENT_IDS_KEY = "agent_ids"
    EVENT_EMITTER_KEY = "event_emitter"

    # Chat history operations
    OP_READ = "retrieve"
    OP_WRITE = "save"

    # Other keys
    IS_MULTIMODAL_KEY = "is_multimodal"
    NEW_ANONYMIZED_MAPPINGS_KEY = "new_anonymized_mappings"
    RESPONSE_KEY = "response"
    QUERY_KEY = "query"
    ORIGINAL_MESSAGE_KEY = "original_message"
    CHAT_HISTORY_KEY = "chat_history"
    OPERATION_KEY = "operation"
    LAST_MESSAGE_ID_KEY = "last_message_id"
    CACHE_HIT_KEY = "cache_hit"

    IS_ERROR_KEY = "is_error"
    IS_FROM_SHARED_CONVERSATION_KEY = "is_from_shared_conversation"
