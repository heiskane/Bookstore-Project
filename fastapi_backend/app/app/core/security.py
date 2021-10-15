from datetime import datetime
from datetime import timedelta
from typing import List

from jose import jwt  # type: ignore[import]
from passlib.context import CryptContext  # type: ignore[import]

from app import models
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def create_access_token(user: models.User, expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {
        "exp": expire,
        "sub": user.username,
        "is_admin": user.is_admin,
        "is_active": user.is_active,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_anon_buyer_token(books: List[models.Book], expires_delta: timedelta) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {
        "exp": expire,
        "sub": "anonymous",
        "ordered_book_ids": [book.id for book in books],
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(password_plain: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plain, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
