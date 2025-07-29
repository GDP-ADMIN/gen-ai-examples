"""Provides RollingKeyBytesEncryptor class which facilitates the encryption and decryption using rolling key mechanism.

It is based on CATAPA RollingKeyBytesEncryptor implementation. The encryption keys can be switched out over time
(rolling keys) and the class is capable of decrypting data encrypted with any of the keys it manages.

Authors:
    Berty C L Tobing (berty.c.l.tobing@gdplabs.id)

References:
    [1] https://github.com/GDP-ADMIN/CATAPA-API/blob/master/common/src/main/java/com/catapa/common/security/encryption/RollingKeyBytesEncryptor.java
    # noqa: E501
"""

from claudia_gpt.config.constant import (
    CATAPA_ENCRYPTION_CURRENTKEYID,
    CATAPA_ENCRYPTION_KEYS_K1_PASSWORD,
    CATAPA_ENCRYPTION_KEYS_K1_SALT,
)
from claudia_gpt.encryption.decryptor.base_decryptor import BaseDecryptor
from claudia_gpt.encryption.encryptor.aes_bytes_encryptor import AesBytesEncryptor


class RollingKeyBytesEncryptor:
    """Provides functionality to encrypt and decrypt data using a rolling key mechanism.

    It supports multiple AES keys and can identify the correct key for decryption based on a prefix.

    Attributes:
        PREFIX_BOUNDARY (str): Delimiter used to identify the key ID within the encrypted data.
        PREFIX_SAMPLE_LENGTH (int): The length to check for the presence of a PREFIX_BOUNDARY.
        bytes_encryptors (dict[str, AesBytesEncryptor]): Dictionary of available encryptors by key ID.
        current_key_id (str): ID of the current key used for encryption.
    """

    PREFIX_BOUNDARY = "$$"
    PREFIX_SAMPLE_LENGTH = 7

    def __init__(self, decryptor: BaseDecryptor):
        """Initialize the RollingKeyBytesEncryptor instance.

        Args:
            decryptor (BaseDecryptor): An instance of the BaseDecryptor class for decrypting environment variables.
        """
        current_key_id = CATAPA_ENCRYPTION_CURRENTKEYID
        k1_password = decryptor.decrypt(CATAPA_ENCRYPTION_KEYS_K1_PASSWORD)
        k1_salt = decryptor.decrypt(CATAPA_ENCRYPTION_KEYS_K1_SALT)

        self.bytes_encryptors = {current_key_id: AesBytesEncryptor.stronger(k1_password, k1_salt)}
        self.current_key_id = current_key_id

    def encrypt(self, data: str) -> bytes:
        """Encrypts a given string.

        Args:
            data (str): The string to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        byte_representation = data.encode("utf-8")
        return self.encrypt_bytes(byte_representation)

    def encrypt_bytes(self, data: bytes) -> bytes:
        """Encrypt a given byte data with the current key and adds a prefix to identify the key used.

        Args:
            data (bytes): The data to be encrypted.

        Returns:
            bytes: The encrypted data with a prefix.
        """
        prefix = f"{self.PREFIX_BOUNDARY}{self.current_key_id}{self.PREFIX_BOUNDARY}"
        prefix_bytes = prefix.encode("utf-8")

        encryptor = self.bytes_encryptors[self.current_key_id]
        encrypted_bytes = encryptor.encrypt(data)

        return prefix_bytes + encrypted_bytes

    def decrypt(self, encrypted_data_with_prefix: bytes) -> bytes:
        """Decrypt the given byte data. Determines the key to use based on the prefix.

        Args:
            encrypted_data_with_prefix (bytes): The data to be decrypted.

        Returns:
            bytes: The decrypted data.
        """
        key_id = self.determine_key_id(encrypted_data_with_prefix)
        return self._decrypt_with_key_id(key_id, encrypted_data_with_prefix)

    @staticmethod
    def determine_key_id(encrypted_data_with_prefix: bytes) -> str:
        """Extract the key ID from the encrypted data's prefix.

        The encrypted data is expected to have the following format:

        BOUNDARY<key_id>BOUNDARY...

        Where:
        - BOUNDARY is a predefined boundary string.
        - <key_id> is the key ID we want to extract.

        Args:
            encrypted_data_with_prefix (bytes): The encrypted data with a prefix.

        Returns:
            str: The key ID if found, otherwise raises a ValueError.

        Raises:
            ValueError: If the key ID doesn't exist.
        """
        prefix_sample_bytes = encrypted_data_with_prefix[: RollingKeyBytesEncryptor.PREFIX_SAMPLE_LENGTH]
        prefix_sample = prefix_sample_bytes.decode("utf-8", "backslashreplace")

        if prefix_sample.startswith(RollingKeyBytesEncryptor.PREFIX_BOUNDARY):
            key_id_begin_index = len(RollingKeyBytesEncryptor.PREFIX_BOUNDARY)
            key_id_end_index = prefix_sample.find(RollingKeyBytesEncryptor.PREFIX_BOUNDARY, key_id_begin_index)
            if key_id_end_index != -1:
                return prefix_sample[key_id_begin_index:key_id_end_index]

        raise ValueError("Key ID does not exist.")

    def _decrypt_with_key_id(self, key_id: str, encrypted_data_with_prefix: bytes) -> bytes:
        """Decrypt the data using the specified key ID.

        Args:
            key_id (str): The key ID.
            encrypted_data_with_prefix (bytes): The encrypted data with a prefix.

        Returns:
            bytes: The decrypted data.
        """
        prefix_length = 2 * len(self.PREFIX_BOUNDARY) + len(key_id)
        encrypted_bytes = encrypted_data_with_prefix[prefix_length:]

        encryptor = self.bytes_encryptors[key_id]
        return encryptor.decrypt(encrypted_bytes)
