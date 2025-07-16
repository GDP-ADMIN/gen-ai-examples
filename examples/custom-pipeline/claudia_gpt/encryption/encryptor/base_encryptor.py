"""Module providing a base class for encryption and decryption operations.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from abc import ABC, abstractmethod
from typing import Any


class BaseEncryptor(ABC):
    """Base class for encryption and decryption."""

    @abstractmethod
    def encrypt(self, **kwargs: Any) -> Any:
        """Encrypt data.

        Args:
            **kwargs (Any): Arguments required for encryption.

        Returns:
            Any: The encrypted data.
        """

    @abstractmethod
    def decrypt(self, **kwargs: Any) -> Any:
        """Decrypt data.

        Args:
            **kwargs (Any): Arguments required for decryption.

        Returns:
            Any: The decrypted data.
        """
