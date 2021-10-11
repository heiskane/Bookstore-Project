from datetime import datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from app.models import User
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated=["auto"])


def create_access_token(user: User, expires_delta: timedelta = None) -> str:
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


def verify_password(password_plain: str, password_hash: str) -> bool:
    return pwd_context.verify(password_plain, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
