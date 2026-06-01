from datetime import datetime, timedelta
from jose import jwt
from typing import Optional
from ..core import config


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = {"sub": subject}
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded


def decode_token(token: str) -> dict:
    return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
