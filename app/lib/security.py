import hashlib


def encrypt_password_to_sha256(password: str) -> str:
    """
    encrypt_password_to_sha256
    """

    return hashlib.sha256(password.encode()).hexdigest()
