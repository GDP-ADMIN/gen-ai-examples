"""Module for handling JWT (JSON Web Token) generation.

This module provides a utility class `CatapaJwtUtil` for generating JWTs with RSA encryption.
The JWTs are signed using a private key, and they have a predefined expiration time set.

Authors:
    Immanuel Rhesa (immanuel.rhesa@gdplabs.id)
"""

import time
from urllib.parse import urlparse

import jks
import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.types import PrivateKeyTypes
from cryptography.hazmat.primitives.serialization.pkcs12 import load_key_and_certificates

from claudia_gpt.analytics.constant import KeystoreType
from claudia_gpt.config.constant import (
    CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PAIR,
    CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PASSWORD,
    CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PATH,
    CATAPA_AUTH_KEYSTORE_TYPE,
)

JWT_DURATION_SECONDS = 2 * 60  # 2 minutes
JWT_ALGORITHM = "RS256"


def generate_jwt() -> str:
    """Generate a JWT with an expiration time.

    This method creates a JWT with a predefined expiration time set in seconds. It signs the token using
    the RSA private key provided during the class initialization.

    Returns:
        str: The generated JWT as a string.

    Raises:
        Exception: If there is an issue in signing the JWT.
    """
    expiration_time = int(time.time()) + JWT_DURATION_SECONDS
    claims = {"exp": expiration_time}
    private_key = _get_private_key()
    token = jwt.encode(claims, private_key, algorithm=JWT_ALGORITHM)
    return token


def _get_private_key() -> PrivateKeyTypes:
    """Retrieve the RSA private key from the specified PKCS12 or JKS file path.

    This method is used internally to load the RSA private key from the file specified during the initialization.
    It expects the key to be in PKCS12 format.

    Returns:
        RSAPrivateKey: The RSA private key.
    """
    # TODO: will remove keystore type if all env already use the same type
    parsed_uri = urlparse(CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PATH)
    key_path = parsed_uri.path
    if CATAPA_AUTH_KEYSTORE_TYPE.upper() == KeystoreType.PKCS12:
        with open(key_path, "rb") as file:
            pkcs12_data = file.read()

        private_key, _, _ = load_key_and_certificates(
            pkcs12_data, password=CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PASSWORD.encode(), backend=default_backend()
        )
    elif CATAPA_AUTH_KEYSTORE_TYPE.upper() == KeystoreType.JKS:
        key_store = jks.KeyStore.load(key_path, CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PASSWORD)
        pk_entry = key_store.private_keys[CATAPA_AUTH_ACCESSTOKEN_JWT_PRIVATEKEY_PAIR]
        private_key = serialization.load_der_private_key(pk_entry.pkey, password=None, backend=default_backend())
    else:
        raise ValueError(f"Unsupported keystore type: {CATAPA_AUTH_KEYSTORE_TYPE}")

    return private_key
