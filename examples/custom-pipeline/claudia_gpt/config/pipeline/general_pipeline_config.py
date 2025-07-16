"""General Pipeline Config.

This config contains the general pipeline config used in all pipelines.

Authors:
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)

References:
    NONE
"""

from enum import StrEnum
from typing import Any

from pydantic import BaseModel

from claudia_gpt.config.constant import DEFAULT_LANG_ID


class GeneralPipelineConfig(BaseModel):
    """A Pydantic model representing the general pipeline config used in all pipelines.

    Attributes:
        model_name (str | None): The model name.
        anonymize_em (bool | None): Whether to anonymize before using the embedding model.
        anonymize_lm (bool | None): Whether to anonymize before using the language model.
        use_cache (bool | None): Whether to check and use cached response, if available.
        search_type (str): The search type.
        knowledge_base_id (str): The knowledge base ID.
        use_docproc (bool): Whether to use the document processing orchestrator.
        attachments (dict[str, Any]): A dictionary containing attachments.
        attachment_chunk_size (int): The attachment chunk size.
        binaries (list[Any]): A list containing binary data objects.
        user_id (str): The user ID.
        conversation_id (str): The conversation ID.
        parent_id (str): The parent ID.
        user_message_id (str): The user message ID.
        assistant_message_id (str): The assistant message ID.
        chat_history (list[Any]): A list containing the chat history.
        source (str): The source.
        start_time (float): The start time.
        lang_id (str): The language ID.
        user_multimodal_contents (list[Any]): A list containing the user multimodal contents.
    """

    model_name: str | None = None
    anonymize_em: bool | None = None
    anonymize_lm: bool | None = None
    use_cache: bool | None = None
    search_type: str
    knowledge_base_id: str = ""
    use_docproc: bool
    attachments: dict[str, Any]
    attachment_chunk_size: int
    binaries: list[Any]
    user_id: str = ""
    conversation_id: str = ""
    parent_id: str = ""
    user_message_id: str = ""
    assistant_message_id: str = ""
    chat_history: list[Any] = []
    source: str = ""
    start_time: float
    lang_id: str = DEFAULT_LANG_ID
    user_multimodal_contents: list[Any] = []

    def __init__(self, request_config: dict[str, Any]):
        """Initialize a GeneralPipelineConfig instance.

        This constructor takes in a request_config dictionary.
        It processes the request_config to set the attributes of the GeneralPipelineConfig instance.

        Args:
            request_config (dict[str, Any]): A dictionary containing request and pipeline_config.

        Raises:
            ValueError: 'support_pii_anonymization' is set to True, but either 'anonymize_em'
                or 'anonymize_lm' is not provided (None).
        """
        support_pii_anonymization = request_config.get("support_pii_anonymization", False)

        anonymize_em = request_config.get("anonymize_em")
        anonymize_lm = request_config.get("anonymize_lm")

        if support_pii_anonymization and (anonymize_em is None or anonymize_lm is None):
            raise ValueError("anonymize_em or anonymize_lm must not be empty.")

        super().__init__(**request_config)


class GeneralPipelineConfigKeys(StrEnum):
    """List of all possible keys in GeneralPipelineConfig."""

    MODEL_NAME = "model_name"
    ANONYMIZE_EM = "anonymize_em"
    ANONYMIZE_LM = "anonymize_lm"
    USE_CACHE = "use_cache"
    SEARCH_TYPE = "search_type"
    KNOWLEDGE_BASE_ID = "knowledge_base_id"
    USE_DOCPROC = "use_docproc"
    ATTACHMENTS = "attachments"
    ATTACHMENT_CHUNK_SIZE = "attachment_chunk_size"
    BINARIES = "binaries"
    USER_ID = "user_id"
    CONVERSATION_ID = "conversation_id"
    PARENT_ID = "parent_id"
    USER_MESSAGE_ID = "user_message_id"
    ASSISTANT_MESSAGE_ID = "assistant_message_id"
    CHAT_HISTORY = "chat_history"
    SOURCE = "source"
    START_TIME = "start_time"
    LANG_ID = "lang_id"
    USER_MULTIMODAL_CONTENTS = "user_multimodal_contents"
