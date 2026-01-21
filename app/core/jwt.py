# app/core/jwt.py

from datetime import datetime, timedelta
from jose import jwt, JWTError
from typing import Optional

from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_SECONDS


def create_access_token(user_id: int) -> str:
    """
    Create JWT token with user_id and expiration
    """
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)

    payload = {"sub": str(user_id), "exp": expire}  # subject = user identifier

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> Optional[int]:
    """
    Decode JWT token and return user_id if valid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")

        if user_id is None:
            return None

        return int(user_id)

    except JWTError:
        return None
