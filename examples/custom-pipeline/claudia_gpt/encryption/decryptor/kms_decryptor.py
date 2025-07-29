"""Provides a concrete decryptor that utilizes AWS KMS for decryption.

This module defines the KMSDecryptor class, which is a concrete decryptor that utilizes AWS Key Management Service (KMS)
for decrypting Base64-encoded ciphertext. The KMSDecryptor class extends the BaseDecryptor class.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

import base64

import boto3

from claudia_gpt.config.constant import CATAPA_ENCRYPTION_KMS_AWS_REGION, CATAPA_ENCRYPTION_KMS_KEYID
from claudia_gpt.encryption.decryptor.base_decryptor import BaseDecryptor


class KMSDecryptor(BaseDecryptor):
    """A concrete decryptor that utilizes AWS KMS for decryption.

    Attributes:
        kms (boto3.client): The KMS client instance.
    """

    def __init__(self):
        """Initialize the KMSDecryptor instance."""
        self.kms = boto3.client("kms", region_name=CATAPA_ENCRYPTION_KMS_AWS_REGION)

    def decrypt(self, base64_ciphertext: str) -> str:
        """Decrypts the provided Base64-encoded ciphertext using AWS KMS.

        Args:
            base64_ciphertext (str): The Base64-encoded encrypted data.

        Returns:
            str: The decrypted data as a string.
        """
        ciphertext_blob = base64.b64decode(base64_ciphertext)

        decrypt_response = self.kms.decrypt(CiphertextBlob=ciphertext_blob, KeyId=CATAPA_ENCRYPTION_KMS_KEYID)
        return decrypt_response.get("Plaintext").decode("utf-8")
