"""DB Model Class for database table.

These classes are used to define the database schemas for the application.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

import uuid

import sqlalchemy as sa

from claudia_gpt.db.adapter import DatabaseAdapter


class AnonymizerMappingModel(DatabaseAdapter.base):
    """Database model for anonymizer mappings.

    This model defines the database schemas for storing anonymized PII data and its mapping to original values.

    Attributes:
        id (Column): Unique identifier for the anonymizer mapping (UUID format).
        conversation_id (Column): Foreign key linking to the 'conversation' table.
        pii_type (Column): Type of Personally Identifiable Information (PII) being anonymized.
        anonymized_value (Column): The anonymized version of the PII data.
        pii_value (Column): The original PII value before anonymization.
    """

    __tablename__ = "anonymizer_mappings"
    id = sa.Column(sa.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = sa.Column(
        sa.String(36), sa.ForeignKey("conversations.id"), nullable=False
    )  # Claudia adjustment: use conversations.id
    pii_type = sa.Column(sa.String(30), nullable=False)
    anonymized_value = sa.Column(sa.String(255), nullable=False)
    pii_value = sa.Column(
        sa.BLOB, nullable=False
    )  # Claudia adjustment: use BLOB for pii_value to handle encrypted data
