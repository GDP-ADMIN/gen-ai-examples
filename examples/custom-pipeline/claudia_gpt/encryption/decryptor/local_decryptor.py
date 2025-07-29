"""Provides a concrete decryptor that implements a custom decryption strategy.

This module defines the LocalDecryptor class, which is a concrete decryptor that implements a custom
decryption strategy. The LocalDecryptor class extends the BaseDecryptor class.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

from claudia_gpt.encryption.decryptor.base_decryptor import BaseDecryptor


class LocalDecryptor(BaseDecryptor):
    """A concrete decryptor that implements a custom decryption strategy."""

    def decrypt(self, base64_ciphertext: str) -> str:
        """Decrypts the provided ciphertext using a custom strategy.

        Args:
        base64_ciphertext (str): The Base64-encoded encrypted data.

        Returns:
            str: The decrypted data as a string.
        """
        return base64_ciphertext
