"""Module providing AES-GCM encryption and decryption using PBKDF2 for key derivation.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)
"""

import base64

from Crypto.Random import get_random_bytes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from claudia_gpt.encryption.base_encryptor import BaseEncryptor


class AesGcmEncryptor(BaseEncryptor):
    """AES-GCM 256 Encryptor using PBKDF2 for key derivation.

    This class provides AES-GCM encryption and decryption methods with a 256-bit key derived using PBKDF2.

    Attributes:
        backend (Any): Cryptographic backend used for key derivation.
        salt (bytes): Salt used for key derivation.
        key (bytes): Derived 256-bit encryption key.
    """

    def __init__(self, password: str, salt: str):
        """Initialize AesGcmEncryptor with a password and salt for key derivation.

        Args:
            password (str): Password used to derive the encryption key.
            salt (str): Hexadecimal salt string used in the key derivation.
        """
        self.backend = default_backend()
        self.salt = bytes.fromhex(salt)
        self.key = self.derive_key(password)  # Define the key once at initialization

    def derive_key(self, password: str) -> bytes:
        """Derive a 256-bit key using PBKDF2HMAC.

        Args:
            password (str): Password to derive the key from.

        Returns:
            bytes: The derived 256-bit encryption key.
        """
        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=self.salt, iterations=100000, backend=self.backend)
        return kdf.derive(password.encode())

    def encrypt(self, plain_text: str) -> str:
        """Encrypts the plain text using AES-GCM with a random nonce.

        Args:
            plain_text (str): The plaintext data to be encrypted.

        Returns:
            str: The encrypted data, encoded in base64 format.
        """
        aesgcm = AESGCM(self.key)
        nonce = get_random_bytes(12)  # 12-byte nonce for AES-GCM
        cipher_text = aesgcm.encrypt(nonce, plain_text.encode(), None)

        encrypted_data = base64.b64encode(self.salt + nonce + cipher_text).decode("utf-8")
        return encrypted_data

    def decrypt(self, cipher_text: str) -> str:
        """Decrypts the AES-GCM encrypted text.

        Args:
            cipher_text (str): The encrypted data in base64 format to be decrypted.

        Returns:
            str: The decrypted plaintext data.
        """
        decoded_data = base64.b64decode(cipher_text)
        nonce = decoded_data[16:28]
        actual_cipher_text = decoded_data[28:]

        aesgcm = AESGCM(self.key)
        decrypted_data = aesgcm.decrypt(nonce, actual_cipher_text, None)
        return decrypted_data.decode("utf-8")
