"""Anonymizer storage module.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)
"""

from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from gllm_plugin.storage.base_anonymizer_storage import BaseAnonymizerStorage, MappingDataType
from gllm_privacy.pii_detector.utils.deanonymizer_mapping import get_dict_diff
from sqlalchemy.exc import SQLAlchemyError

from claudia_gpt.anonymizer.models import AnonymizerMappingModel
from claudia_gpt.anonymizer.schemas import AnonymizerMapping
from claudia_gpt.encryption.encryptor.base_encryptor import (
    BaseEncryptor,  # Claudia adjustment: use encryptor.BaseEncryptor
)
from claudia_gpt.utils.logger import logger


class AnonymizerStorage(BaseAnonymizerStorage):
    """Class for handling anonymizer.

    This class acts as a service layer to interact with the data store for anonymizer operations.
    """

    def __init__(self, data_store: SQLAlchemySQLDataStore, encryptor: BaseEncryptor):
        """Initialize the AnonymizerStorage with a data store instance.

        Args:
            data_store (SQLAlchemySQLDataStore): The data store instance to interact with for data operations.
            encryptor (BaseEncryptor): The encryptor instance for encrypting and decrypting PII values.
        """
        self.data_store = data_store
        self.db = data_store.db
        self.encryptor = encryptor

    def get_mappings_by_conversation_id(self, conversation_id: str) -> list[AnonymizerMapping]:
        """Retrieve anonymizer mappings by conversation ID.

        Args:
            conversation_id (str): The unique identifier for the conversation.

        Returns:
            list[AnonymizerMapping]: A list of anonymizer mappings associated with the given conversation ID.
        """
        with self.db() as session:
            try:
                mappings = (
                    session.query(AnonymizerMappingModel)
                    .filter(AnonymizerMappingModel.conversation_id == conversation_id)
                    .all()
                )
            except SQLAlchemyError as exc:
                logger.error(f"Failed to get anonymizer mappings: {exc}")
                return []

            decrypted_mappings: list[AnonymizerMapping] = []
            # Claudia adjustment: decrypt the PII value
            for obj in mappings:
                try:
                    obj.pii_value = self.encryptor.decrypt(cipher_text=obj.pii_value).decode("utf-8")
                except Exception as e:
                    obj.pii_value = obj.anonymized_value
                    logger.error(f"Failed to decrypt PII value: {e}")

                anonymizer_mapping = AnonymizerMapping.model_validate(obj)

                decrypted_mappings.append(anonymizer_mapping)

            return decrypted_mappings

    def create_mapping(
        self, conversation_id: str, pii_type: str, anonymized_value: str, pii_value: str
    ) -> AnonymizerMapping:
        """Create a new anonymizer mapping.

        Args:
            conversation_id (str): The unique identifier for the conversation.
            pii_type (str): The type of Personally Identifiable Information (PII) to be anonymized.
            anonymized_value (str): The anonymized version of the PII.
            pii_value (str): The original PII value.

        Returns:
            AnonymizerMapping: The newly created anonymizer mapping instance.
        """
        with self.db() as session:
            try:
                encrypted_pii_value: str = self.encryptor.encrypt(
                    plain_text=pii_value
                )  # Claudia adjustment: use kwargs

                new_mapping = AnonymizerMappingModel(
                    conversation_id=conversation_id,
                    pii_type=pii_type,
                    anonymized_value=anonymized_value,
                    pii_value=encrypted_pii_value,
                )
                session.add(new_mapping)
                session.commit()
                session.refresh(new_mapping)

                new_mapping.pii_value = pii_value  # Claudia adjustment: set the original PII value
                return AnonymizerMapping.model_validate(new_mapping)
            except SQLAlchemyError as exc:
                logger.error(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    # Claudia adjustment: Implement update_mapping method
    def update_mapping(self, conversation_id: str, is_anonymized: bool, mapping_data_type: MappingDataType) -> None:
        """Update the mappings for a specific conversation with new anonymizer mappings.

        Args:
            conversation_id (str): The unique identifier for the conversation.
            is_anonymized (bool): The flag to determine if the message is anonymized.
            mapping_data_type (MappingDataType): A dictionary of new anonymizer mappings to update for deanonymization.
        """
        if is_anonymized:
            saved_mappings = self.get_mappings_by_conversation_id(conversation_id)
            saved_anonymizer_mappings = AnonymizerMapping.convert_to_mapping_data_type(saved_mappings)

            new_mappings = get_dict_diff(saved_anonymizer_mappings, mapping_data_type)
            for mapping in new_mappings:
                self.create_mapping(
                    conversation_id=conversation_id,
                    pii_type=mapping["pii_type"],
                    anonymized_value=mapping["anonymized_value"],
                    pii_value=mapping["pii_value"],
                )
