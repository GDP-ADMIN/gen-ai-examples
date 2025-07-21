"""Constant for the API.

Authors:
    Ryan Ignatius Hadiwijaya (ryan.i.hadiwijaya@gdplabs.id)

References:
    None
"""

from enum import StrEnum


class SearchType(StrEnum):
    """The type of search to perform.

    Attributes:
        NORMAL: Get answer from chatbot knowledge.
        SMART: Get more relevant information from your stored documents and knowledge base.
            Knowledge Search is an AI with specialized knowledge. No agents are available in this mode.
        WEB: Get more relevant information from the web.
            Web Search uses real-time data. Agent selection isn't available in this mode.
    """

    NORMAL = "normal"
    SMART = "smart"
    WEB = "web"


class LangId(StrEnum):
    """The language id.

    Attributes:
        EN: Id for English language.
        ID: Id for Indonesian language.
    """

    EN = "en"
    ID = "id"


class ReferenceFormatterType(StrEnum):
    """The type of reference formatter to use.

    Attributes:
        SIMILARITY: Use similarity based reference formatter.
        LM: Use LM based reference formatter.
        NONE: No reference formatter is used.
    """

    SIMILARITY = "similarity"
    LM = "lm"
    NONE = "none"


class ExportType(StrEnum):
    """The type of export to perform.

    Attributes:
        XLSX: Export to XLSX.
        CSV: Export to CSV.
    """

    XLSX = "xlsx"
    CSV = "csv"


class StepIndicatorStatus(StrEnum):
    """Class containing step indicator status constants."""

    RUNNING = "running"
    FINISHED = "finished"


class StepIndicatorId:
    """Class containing step indicator id constants."""

    PROCESSING_ATTACHMENTS = {LangId.EN: "Processing file(s)", LangId.ID: "Memproses file"}
    UNDERSTANDING_QUERY = {LangId.EN: "Understanding question", LangId.ID: "Memahami pertanyaan"}
    MASKING_PRIVATE_DATA_QUERY = {
        LangId.EN: "Masking private data in the question",
        LangId.ID: "Menyamarkan data pribadi dalam pertanyaan",
    }
    MASKING_PRIVATE_ATTACHMENTS_CONTEXT = {
        LangId.EN: "Masking private data in file(s)",
        LangId.ID: "Menyamarkan data pribadi dalam file",
    }
    MASKING_PRIVATE_CONTEXT = {
        LangId.EN: "Masking private data in retrieved knowledge",
        LangId.ID: "Menyamarkan data pribadi dalam informasi yang ditemukan",
    }
    RETRIEVING_KNOWLEDGE = {LangId.EN: "Retrieving data", LangId.ID: "Mengambil data"}
    GENERATING_RESPONSE = {LangId.EN: "Generating answer", LangId.ID: "Mempersiapkan jawaban"}
    FORMATTING_REFERENCE = {LangId.EN: "Determining relevant sources", LangId.ID: "Menentukan sumber data yang relevan"}
