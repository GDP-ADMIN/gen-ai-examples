"""Provides an abstract class representing a decryptor.

This module defines the BaseDecryptor class, representing a decryptor. Any new decryption
strategy should extend this class.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from abc import ABC, abstractmethod


class BaseDecryptor(ABC):
    """Base class representing a decryptor. Any new decryption strategy should extend this class."""

    @abstractmethod
    def decrypt(self, base64_ciphertext: str) -> str:
        """Decrypts the provided ciphertext.

        Args:
        base64_ciphertext (str): The Base64-encoded encrypted data.

        Returns:
            str: The decrypted data as a string.
        """
