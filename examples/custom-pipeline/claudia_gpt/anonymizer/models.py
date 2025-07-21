"""DB Model Class for database table.

These classes are used to define the database schema for the application.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

import uuid

import sqlalchemy as sa
from gllm_datastore.sql_data_store.adapter.sqlalchemy_adapter import SQLAlchemyAdapter


class AnonymizerMappingModel(SQLAlchemyAdapter.base):
    """Database model for anonymizer mappings.

    This model defines the database schema for storing anonymized PII data and its mapping to original values.

    Attributes:
        id (Column): Unique identifier for the anonymizer mapping (UUID format).
        conversation_id (Column): Foreign key linking to the 'conversation' table.
        pii_type (Column): Type of Personally Identifiable Information (PII) being anonymized.
        anonymized_value (Column): The anonymized version of the PII data.
        pii_value (Column): The original PII value before anonymization.
    """

    __table_args__ = {"extend_existing": True}
    __tablename__ = "anonymizer_mapping"
    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = sa.Column(sa.String(36), sa.ForeignKey("conversation.id"), nullable=False)
    pii_type = sa.Column(sa.String(30), nullable=False)
    anonymized_value = sa.Column(sa.String(255), nullable=False)
    pii_value = sa.Column(sa.TEXT, nullable=False)
