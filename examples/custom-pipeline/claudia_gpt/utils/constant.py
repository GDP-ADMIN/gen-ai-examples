"""Constants for Claudia pipeline.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)
"""

from claudia_gpt.component.chat_history_manager import ChatHistoryManager
from claudia_gpt.utils.initializer import get_anonymizer_storage, get_chat_history_storage

anonymizer_storage = get_anonymizer_storage()
chat_history_storage = get_chat_history_storage()
chat_history_manager = ChatHistoryManager(storage=chat_history_storage, anonymizer_storage=anonymizer_storage)
