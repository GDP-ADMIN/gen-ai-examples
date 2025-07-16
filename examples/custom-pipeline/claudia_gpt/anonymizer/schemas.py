"""Anonymizer related models.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from collections import defaultdict

from gllm_privacy.pii_detector.utils.deanonymizer_mapping import MappingDataType
from pydantic import BaseModel, ConfigDict


class AnonymizerMapping(BaseModel):
    """Anonymizer mapping model.

    This model represents the mapping of anonymized values with their corresponding PII types and values.

    Attributes:
        id (str): Unique identifier for the mapping.
        conversation_id (str): Identifier for the conversation associated with this mapping.
        pii_type (str): Type of Personally Identifiable Information (PII) being anonymized.
        anonymized_value (str): The anonymized version of the PII data.
        pii_value (str): The original PII value before anonymization.
    """

    model_config = ConfigDict(from_attributes=True)

    id: str
    conversation_id: str
    pii_type: str
    anonymized_value: str
    pii_value: str

    @staticmethod
    def convert_to_mapping_data_type(mappings: list["AnonymizerMapping"]) -> MappingDataType:
        """Converts a list of AnonymizerMapping objects into a dictionary of dictionaries.

        Args:
            mappings (list[AnonymizerMapping]): List of AnonymizerMapping objects.

        Returns:
            MappingDataType: A dictionary with PII types as keys and mappings of anonymized values to PII values.
        """
        result: MappingDataType = defaultdict(lambda: defaultdict(str))

        for mapping in mappings:
            result[mapping.pii_type][mapping.anonymized_value] = mapping.pii_value

        return result
