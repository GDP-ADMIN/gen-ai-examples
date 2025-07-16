"""Module providing the CatapaEncryptor class for AES-GCM encryption and decryption.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from typing import Any

from claudia_gpt.encryption.encryptor.base_encryptor import BaseEncryptor
from claudia_gpt.encryption.encryptor.rolling_key_bytes_encryptor import RollingKeyBytesEncryptor


class CatapaEncryptor(BaseEncryptor):
    """Encryptor class for AES-GCM encryption and decryption.

    Uses a rolling key encryption scheme with AES-GCM for secure encryption and decryption.

    Attributes:
        _rolling_key_bytes_encryptor (RollingKeyBytesEncryptor): Instance used for encryption and decryption operations.
    """

    def __init__(self, rolling_key_bytes_encryptor: RollingKeyBytesEncryptor):
        """Initialize CatapaEncryptor with a given encryption key.

        Args:
            rolling_key_bytes_encryptor (RollingKeyBytesEncryptor): The encryptor instance to use for encryption and
                decryption.
        """
        self._rolling_key_bytes_encryptor = rolling_key_bytes_encryptor

    def encrypt(self, **kwargs: Any) -> Any:
        """Encrypt data using AES-GCM.

        Args:
            **kwargs (Any):
                plain_text (str): Data to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        plain_text = kwargs.get("plain_text")
        return self._rolling_key_bytes_encryptor.encrypt(plain_text)

    def decrypt(self, **kwargs: Any) -> Any:
        """Decrypt data using AES-GCM.

        Args:
            **kwargs (Any):
                cipher_text (bytes): Data to be decrypted.

        Returns:
            bytes: The decrypted data.
        """
        cipher_text = kwargs.get("cipher_text")
        return self._rolling_key_bytes_encryptor.decrypt(cipher_text)
