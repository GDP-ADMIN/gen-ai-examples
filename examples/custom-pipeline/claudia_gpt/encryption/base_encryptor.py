"""Module providing an abstract base class for encryption and decryption operations.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from abc import ABC, abstractmethod


class BaseEncryptor(ABC):
    """Base class for encryption and decryption."""

    @abstractmethod
    def encrypt(self, plain_text: str) -> str:
        """Encrypt the given plain text.

        Args:
            plain_text (str): The text to be encrypted.

        Returns:
            str: The encrypted text.
        """

    @abstractmethod
    def decrypt(self, cipher_text: str) -> str:
        """Decrypt the given cipher text.

        Args:
            cipher_text (str): The encrypted data.

        Returns:
            str: The decrypted plain text.
        """
