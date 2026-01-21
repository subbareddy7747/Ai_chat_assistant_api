# app/core/security.py
from argon2 import PasswordHasher
from argon2.exceptions import (
    VerifyMismatchError,
)  # pyright: ignore[reportMissingImports]

ph = PasswordHasher()


def get_password_hash(password: str) -> str:
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        ph.verify(hashed_password, plain_password)
        return True
    except VerifyMismatchError:
        return False


def get_user(db, username: str):
    """Get a user from the database."""
    if username in db:
        user_dict = db[username]
        return user_dict  # type: ignore


def authenticate_user(fake_db, username: str, password: str):
    """Check if username and password are correct."""
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
