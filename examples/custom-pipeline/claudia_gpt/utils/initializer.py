"""Helper module.

This module contains helper functions for the FastAPI application.

Authors:
    Anggara Setiawan (anggara.t.setiawan@gdplabs.id)
    Dimitrij Ray (dimitrij.ray@gdplabs.id)

References:
    None
"""

from enum import StrEnum
from typing import Any

from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from gllm_misc.chat_history_manager import ChatHistoryManager as SDKChatHistoryManager
from gllm_retrieval.reranker.reranker import BaseReranker
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

from claudia_gpt.anonymizer.anonymizer_storage import (
    AnonymizerStorage,
)
from claudia_gpt.api.helper.shared_conversation import (
    SharedConversationManager,
)
from claudia_gpt.chat_history import ChatHistoryStorage
from claudia_gpt.config.constant import (
    COHERE_API_KEY,
    COHERE_MODEL,
    ENCRYPTION_PASSWORD,
    ENCRYPTION_SALT,
    GLCHAT_DB_SCHEMA,
    GLCHAT_DB_URL,
)
from claudia_gpt.config.schemas.reranker_schema import CohereRerankerConfig
from claudia_gpt.encryption.aes_gcm_encryptor import (
    AesGcmEncryptor,
)
from claudia_gpt.reranker.cohere_reranker import CohereReranker
from claudia_gpt.reranker.no_op_reranker import NoOpReranker

text_analyzer = None
rolling_key_bytes_encryptor = None  # Claudia adjustment
chat_history_storage = None
anonymizer_storage = None
shared_conversation_manager = None
report_template_storage = None
regulation_document_storage = None
encryptor = AesGcmEncryptor(password=ENCRYPTION_PASSWORD, salt=ENCRYPTION_SALT)

sdk_chat_history_manager: SDKChatHistoryManager | None = None


class RerankerType(StrEnum):
    """The type of reranker.

    Values:
        FLAG_EMBEDDING: The flag embedding reranker.
        COHERE: The Cohere reranker.
        NO_OP: The no-op reranker.
    """

    FLAG_EMBEDDING = "flag_embedding"
    COHERE = "cohere"
    NO_OP = "no_op"


# Custom implementation for Claudia
def get_reranker(type: RerankerType, **kwargs: Any) -> BaseReranker | None:  # noqa: ARG001
    """Get reranker based on keyword arguments.

    Args:
        type (RerankerType): The type of reranker.
        kwargs (Any): The keyword arguments.

    Returns:
        BaseReranker | None : The reranker.
    """
    if type == RerankerType.COHERE:
        return CohereReranker(CohereRerankerConfig(api_key=COHERE_API_KEY, model=COHERE_MODEL))

    if type == RerankerType.NO_OP:
        return NoOpReranker()

    return None


def init_storage(db_url: str | None) -> None:
    """Initialize the chat history and anonymizer storage.

    Args:
        db_url (str | None): The database URL.
    """
    if db_url:
        global sdk_chat_history_manager, chat_history_storage, anonymizer_storage, shared_conversation_manager  # noqa: PLW0603

        if GLCHAT_DB_SCHEMA:
            db_url = f"{db_url}?options=-c%20search_path%3D{GLCHAT_DB_SCHEMA}"

        data_store = SQLAlchemySQLDataStore(engine_or_url=db_url)
        SQLAlchemyInstrumentor().instrument(engine=data_store.engine)
        chat_history_storage = ChatHistoryStorage(data_store=data_store, text_analyzer=text_analyzer)
        anonymizer_storage = AnonymizerStorage(data_store=data_store, encryptor=encryptor)
        shared_conversation_manager = SharedConversationManager(chat_history_storage)
        sdk_chat_history_manager = SDKChatHistoryManager(data_store=data_store)
        # init_admin_service(data_store)


def get_anonymizer_storage() -> AnonymizerStorage:
    """Get the anonymizer storage.

    Returns:
        AnonymizerStorage: The anonymizer storage.
    """
    return anonymizer_storage


def get_chat_history_storage() -> ChatHistoryStorage:
    """Get the chat history storage.

    Returns:
        ChatHistoryStorage: The chat history storage.
    """
    return chat_history_storage


def get_sdk_chat_history_manager() -> SDKChatHistoryManager:
    """Get the chat history manager.

    Returns:
        ChatHistoryManager: The chat history manager.
    """
    return sdk_chat_history_manager


init_storage(GLCHAT_DB_URL)
