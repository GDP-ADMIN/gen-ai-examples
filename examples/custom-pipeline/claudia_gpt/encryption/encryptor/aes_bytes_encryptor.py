"""Provides a tool, `AesBytesEncryptor`, that facilitates encryption and decryption of bytes using AES with GCM modes.

It uses PBKDF2 for key derivation based on a user-provided password and salt.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)

References:
    [1] https://github.com/spring-projects/spring-security/blob/5.3.13.RELEASE/crypto/src/main/java/org/springframework
        /security/crypto/encrypt/AesBytesEncryptor.java # noqa: B950
"""

from os import urandom
from typing import Callable

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class AesBytesEncryptor:
    """Handles encryption and decryption of bytes using AES in GCM mode.

    Attributes:
        secret_key (bytes): Derived key from PBKDF2.
        iv_generator (callable): Function to generate Initialization Vector (IV).
    """

    def __init__(self, password: str, salt: str, iv_generator: Callable[[], bytes]):
        """Initializes the encryptor.

        Args:
            password (str): Password for key derivation.
            salt (str): Salt value for key derivation. Expected in hexadecimal format.
            iv_generator (callable): Function to generate Initialization Vector (IV).
        """
        salt_bytes = bytes.fromhex(salt)

        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA1(), length=32, salt=salt_bytes, iterations=1024, backend=default_backend()
        )

        key = kdf.derive(password.encode("utf-8"))
        self.secret_key = key
        self.iv_generator = iv_generator

    def encrypt(self, plaintext_bytes: bytes) -> bytes:
        """Encrypts the provided plaintext bytes.

        Args:
            plaintext_bytes (bytes): Data to be encrypted.

        Returns:
            bytes: Encrypted data.
        """
        iv = self.iv_generator()
        cipher = self._create_cipher(iv)

        encryptor = cipher.encryptor()
        ct = encryptor.update(plaintext_bytes) + encryptor.finalize()
        return iv + ct + encryptor.tag

    def decrypt(self, encrypted_bytes: bytes) -> bytes:
        """Decrypts the provided ciphertext bytes.

        Args:
            encrypted_bytes (bytes): Data to be decrypted.

        Returns:
            bytes: Decrypted data.
        """
        iv = encrypted_bytes[:16]

        tag = encrypted_bytes[-16:]
        ct = encrypted_bytes[16:-16]
        cipher = self._create_cipher(iv, tag=tag)
        decryptor = cipher.decryptor()

        return decryptor.update(ct) + decryptor.finalize()

    def _create_cipher(self, iv: bytes, tag: bytes | None = None) -> Cipher:
        """Creates and returns a cipher instance based on the chosen AES mode.

        Args:
            iv (bytes): Initialization Vector for the cipher.
            tag (bytes | None): Authentication tag for GCM mode.

        Returns:
            Cipher: Instance of the appropriate cipher.
        """
        return Cipher(algorithms.AES(self.secret_key), modes.GCM(iv, tag), backend=default_backend())

    @staticmethod
    def stronger(password: str, salt: str) -> "AesBytesEncryptor":
        """Factory method to create an instance with GCM mode (stronger encryption).

        Args:
            password (str): Password for key derivation.
            salt (str): Salt value for key derivation.

        Returns:
            AesBytesEncryptor: Instance using GCM mode.
        """
        return AesBytesEncryptor(password, salt, lambda: urandom(16))
