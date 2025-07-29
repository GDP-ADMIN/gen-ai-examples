"""This module contains the constants for the message helper.

Authors:
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

ATTACHMENT_CHUNK_SIZE = 50


QUOTE_REPLY_FORMAT = "Regarding this <quote>{quote}</quote>, please reply to the user's query: <query>{query}</query>"
QUOTE_HISTORY_FORMAT = "Regarding this <quote>{quote}</quote>, the user is asking: <query>{query}</query>"


class PipelineEventKeys:
    """This class contains the keys for the pipeline event."""

    PROCESS = "process"
    ERROR = "error"
    DEANONYMIZED_DATA = "deanonymized_data"
    ATTACHMENTS = "attachments"
    SEARCH_TYPE_CHANGES = "search_type_changes"
    REFERENCE = "reference"
    RELATED = "related"
    MEDIA_MAPPING = "media_mapping"
