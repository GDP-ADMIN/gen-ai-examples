"""Anonymizer storage module.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
    Irvan Ariyanto (irvan.ariyanto@gdplabs.id)
    Felicia Limanta (felicia.limanta@gdplabs.id)
"""

from glchat_plugin.storage.base_anonymizer_storage import BaseAnonymizerStorage, MappingDataType
from gllm_datastore.sql_data_store import SQLAlchemySQLDataStore
from sqlalchemy.exc import SQLAlchemyError

from claudia_gpt.anonymizer.models import AnonymizerMappingModel
from claudia_gpt.anonymizer.schemas import AnonymizerMapping
from claudia_gpt.encryption.base_encryptor import BaseEncryptor
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
            for obj in mappings:
                anonymizer_mapping = AnonymizerMapping.model_validate(obj)

                try:
                    decrypted_pii_value = self.encryptor.decrypt(anonymizer_mapping.pii_value)
                except Exception as e:
                    decrypted_pii_value = anonymizer_mapping.anonymized_value
                    logger.error(f"Failed to decrypt PII value: {e}")

                anonymizer_mapping.pii_value = decrypted_pii_value
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
                encrypted_pii_value: str = self.encryptor.encrypt(pii_value)

                new_mapping = AnonymizerMappingModel(
                    conversation_id=conversation_id,
                    pii_type=pii_type,
                    anonymized_value=anonymized_value,
                    pii_value=encrypted_pii_value,
                )
                session.add(new_mapping)
                session.commit()
                session.refresh(new_mapping)

                return AnonymizerMapping.model_validate(new_mapping)
            except SQLAlchemyError as exc:
                logger.error(f"Failed to commit the transaction: {exc}")
                session.rollback()
                raise exc

    def update_mapping(self, conversation_id: str, is_anonymized: bool, mapping_data_type: MappingDataType) -> None:
        """Update the mappings for a specific conversation with new anonymizer mappings.

        Args:
            conversation_id (str): The unique identifier for the conversation.
            is_anonymized (bool): The flag to determine if the message is anonymized.
            mapping_data_type (MappingDataType): A dictionary of new anonymizer mappings to update for deanonymization.
        """
        pass

    def clone_mappings_to_conversation(self, source_conversation_id: str, target_conversation_id: str) -> None:
        """Clone PII mappings from source conversation to target conversation.

        Args:
            source_conversation_id (str): The source conversation ID.
            target_conversation_id (str): The target conversation ID.
        """
        with self.db() as session:
            try:
                source_mappings = (
                    session.query(AnonymizerMappingModel)
                    .filter(AnonymizerMappingModel.conversation_id == source_conversation_id)
                    .all()
                )

                if not source_mappings:
                    logger.info(f"No PII mappings to clone from {source_conversation_id}")
                    return

                new_mappings = [
                    AnonymizerMappingModel(
                        conversation_id=target_conversation_id,
                        pii_type=mapping.pii_type,
                        anonymized_value=mapping.anonymized_value,
                        pii_value=mapping.pii_value,  # Already encrypted
                    )
                    for mapping in source_mappings
                ]

                session.add_all(new_mappings)
                session.commit()

                logger.info(
                    f"Cloned {len(new_mappings)} PII mappings from {source_conversation_id} "
                    f"to {target_conversation_id}"
                )

            except SQLAlchemyError as exc:
                session.rollback()
                logger.warning(f"Failed to clone PII mappings: {exc}")
                raise
