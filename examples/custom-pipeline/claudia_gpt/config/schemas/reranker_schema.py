"""The schema for the reranker configuration.

Authors:
    Muhammad Afif Al Hawari (muhammad.a.a.hawari@gdplabs.id)

References:
    [1] https://docs.pydantic.dev/latest/
"""

from enum import Enum

from pydantic import BaseModel


class RerankerType(Enum):
    """The enum for the reranker type."""

    NO_OP = "no_op"
    COHERE = "cohere"

    def __str__(self) -> str:
        """Return the string representation of the reranker type."""
        return self.value


class CohereRerankerConfig(BaseModel):
    """Defines the configuration for the Cohere reranker.

    Attributes:
        api_key (str): The API key for Cohere.
        model (str): The model name for Cohere.
    """

    api_key: str
    model: str


class RerankerConfig(BaseModel):
    """Reranker configuration.

    Attributes:
        type (str): The type of the reranker.
    """

    type: RerankerType
    cohere: CohereRerankerConfig | None = None

    class Config:
        """Pydantic configuration model configuration."""

        use_enum_values = True
