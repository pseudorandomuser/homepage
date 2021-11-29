import hmac
import secrets
import hashlib
import binascii

from typing import Optional, Tuple

from flask import current_app as app


def create_secret() -> str:
    secret_length: int = app.config['SECRET_LENGTH']
    return secrets.token_hex(secret_length)


def sign(message: str) -> str:
    app_secret: str = app.config['SECRET_KEY']
    hmac_key: bytes = bytes.fromhex(app_secret)
    hmac_digest: str = app.config['HASH_ALGORITHM']
    hmac_message: bytes = message.encode('UTF-8')
    hmac_instance: hmac.HMAC = hmac.new(
        hmac_key,
        msg=hmac_message,
        digestmod=hmac_digest
    )
    return hmac_instance.hexdigest()


def prepare_password(
    password: str,
    salt: Optional[str] = None
) -> Tuple[str, str]:
    hash_salt: str = salt if salt else create_secret()
    hash_salt_bytes: bytes = bytes.fromhex(hash_salt)
    hash_password_bytes: bytes = password.encode('UTF-8')
    hash_algorithm: str = app.config['HASH_ALGORITHM']
    hash_iterations: int = app.config['HASH_ITERATIONS']
    prepared: bytes = hashlib.pbkdf2_hmac(
        hash_algorithm,
        hash_password_bytes,
        hash_salt_bytes,
        hash_iterations
    )
    prepared_hex: str = binascii.hexlify(prepared).decode('ascii')
    return (prepared_hex, hash_salt)
