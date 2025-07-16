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
from gllm_retrieval.reranker.reranker import BaseReranker

from claudia_gpt.chat_history.chat_history_storage import ChatHistoryStorage
from claudia_gpt.config.constant import COHERE_API_KEY, COHERE_MODEL, DB_URL
from claudia_gpt.config.schemas.reranker_schema import CohereRerankerConfig
from claudia_gpt.reranker.cohere_reranker import CohereReranker
from claudia_gpt.reranker.no_op_reranker import NoOpReranker


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


text_analyzer = None
rolling_key_bytes_encryptor = None  # Claudia adjustment
chat_history_storage = None
anonymizer_storage = None
shared_conversation_manager = None
report_template_storage = None
regulation_document_storage = None


def init_storage(db_url: str | None) -> None:
    """Initialize the chat history and anonymizer storage.

    Args:
        db_url (str | None): The database URL.
    """
    if db_url:
        global chat_history_storage, anonymizer_storage, shared_conversation_manager, report_template_storage, regulation_document_storage  # noqa: PLW0603, E501
        data_store = SQLAlchemySQLDataStore(
            engine_or_url=db_url, pool_pre_ping=True
        )  # Claudia adjustment: add pool_pre_ping=True
        chat_history_storage = ChatHistoryStorage(
            data_store=data_store, text_analyzer=text_analyzer, rolling_key_bytes_encryptor=rolling_key_bytes_encryptor
        )
        # anonymizer_storage = AnonymizerStorage(data_store=data_store, encryptor=encryptor)
        # shared_conversation_manager = SharedConversationManager(chat_history_storage)
        # init_admin_service(db_url)
        # CLaudia adjustment
        # report_template_repository = SqlAlchemyReportGptTemplateRepository(
        #     data_store=data_store, rolling_key_bytes_encryptor=rolling_key_bytes_encryptor
        # )
        # report_template_storage = ReportGptTemplateStorage(report_template_repository)
        # logger.info(f"Report template storage initialized with repository: {report_template_storage}")
        # regulation_document_repository = SqlAlchemyRegulationDocumentRepository(data_store=data_store)
        # regulation_document_storage = RegulationDocumentStorage(regulation_document_repository)


def get_chat_history_storage() -> ChatHistoryStorage | None:
    """Get the chat history storage.

    Returns:
        ChatHistoryStorage | None: The chat history storage.
    """
    return chat_history_storage

init_storage(DB_URL)
