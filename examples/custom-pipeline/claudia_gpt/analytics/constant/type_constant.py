"""Provides enumerations and constants related to type.

Authors:
    Richard Gunawan (richard.gunawan@gdplabs.id)
"""

from enum import Enum, StrEnum


class DataRetrieverType(Enum):
    """Enumeration of data retriever type.

    Attributes:
        CATAPA (str): CATAPA data retriever.
    """

    CATAPA = "catapa"


class KeystoreType:
    """Enumeration of keystore type.

    Attributes:
        PKCS12 (str): PKCS12 key.
        JKS (str): JKS key.
    """

    PKCS12 = "PKCS12"
    JKS = "JKS"


class FileServiceType(Enum):
    """Enumeration of file service types.

    Attributes:
        CATAPA (str): Represents a catapa file service.
        LOCAL (str): Represents a local file service.
    """

    CATAPA = "catapa"
    LOCAL = "local"


class FileExtension(Enum):
    """Enumeration of file extension.

    Attributes:
        XLSX (str): xlsx extension.
        PNG (str): png file extension.
    """

    XLSX = "XLSX"
    PNG = "PNG"


class PromptSourceType(Enum):
    """Enumeration of prompt source type.

    Attributes:
        DATABASE (str): Database prompt source.
        TEST (str): Test prompt source.
    """

    DATABASE = "database"
    TEST = "test"


class AuthorizationTokenType(Enum):
    """Enumeration of authorization token types.

    Attributes:
        HEADER (str): Represents a header authorization token.
    """

    HEADER = "header"


class DataTrusteeType(Enum):
    """Enumeration of data trustee types.

    Attributes:
        CATAPA (str): Represents the CATAPA data trustee type.
        NO_OP (str): Represents a no-operation state where no data trustee used.
    """

    CATAPA = "catapa"
    NO_OP = "no_op"


class AthenaQueryFormatterType(Enum):
    """Enumeration for Athena query formatter types.

    Attributes:
        CATAPA (str): Represents the CATAPA query formatter type.
        NO_OP (str): Represents a no-operation query formatter type.
    """

    CATAPA = "catapa"
    NO_OP = "no_op"


class TrinoQueryFormatterType(Enum):
    """Enumeration for Trino query formatter types.

    Attributes:
        CATAPA (str): Represents the CATAPA query formatter type.
        NO_OP (str): Represents a no-operation query formatter type.
    """

    CATAPA = "catapa"
    NO_OP = "no_op"


class PlotProviderType:
    """Enumeration of plot provider types.

    Attributes:
        LOCAL (str): Represents a local plot provider.
        CATAPA (str): Represents an CATAPA API plot provider.
    """

    LOCAL = "local"
    CATAPA = "catapa"


class ThpSimulatorType(Enum):
    """Enumeration of THP simulator types.

    Attributes:
        CATAPA (str): Represents the CATAPA THP simulator type.
    """

    CATAPA = "catapa"


class PredictiveType(StrEnum):
    """Enumeration of predictive types.

    Attributes:
        PREDEFINED (str): Represents a predefined predictive type.
        LLM (str): Represents a large language model predictive type.
    """

    PREDEFINED = "predefined"
    LLM = "llm"


class PredictionFrequency(Enum):
    """Enumeration of prediction frequency types.

    Attributes:
        DAILY (str): Represents a daily prediction frequency.
        WEEKLY (str): Represents a weekly prediction frequency.
        MONTHLY (str): Represents a monthly prediction frequency.
        QUARTERLY (str): Represents a quarterly prediction frequency.
        YEARLY (str): Represents a monthly prediction frequency.
    """

    DAILY = "DAILY"
    WEEKLY = "WEEKLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    YEARLY = "YEARLY"


class DataFormatType(Enum):
    """Enumeration of data formatting types.

    Attributes:
        POSITIVE_INTEGER (str): Represents positive integer formatting for count-based metrics.
        INTEGER (str): Represents integer formatting for general count data.
        FLOAT (str): Represents float formatting for decimal values.
        PERCENTAGE (str): Represents percentage formatting for percentage values.
    """

    POSITIVE_INTEGER = "positive_integer"
    INTEGER = "integer"
    FLOAT = "float"
    PERCENTAGE = "percentage"
