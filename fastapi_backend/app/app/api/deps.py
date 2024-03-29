from typing import Generator
from typing import Optional

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError  # type: ignore[import]
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from app import crud
from app import models
from app import schemas
from app.async_db.async_database import async_session
from app.core.config import settings
from app.database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login", auto_error=False)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db() -> AsyncSession:
    async with async_session() as session:
        async with session.begin():
            yield session


# https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
async def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> models.User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_name(db=db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# https://stackoverflow.com/questions/66254024/fastapi-optional-oauth2-authentication
async def get_current_user_or_none(
    db: Session = Depends(get_db), token: str = Depends(optional_oauth2_scheme)
) -> Optional[models.User]:
    if not token:
        return None
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = schemas.TokenData(username=username)
    except JWTError:
        return None
    user = crud.get_user_by_name(db=db, username=token_data.username)
    return user


def get_ordered_books_token(
    token: str = Depends(optional_oauth2_scheme),
) -> Optional[str]:
    if not token:
        return None

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        ordered_books: str = payload.get("ordered_book_ids")
        if ordered_books is None:
            return None
    except JWTError:
        return None

    return ordered_books


def require_admin(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
) -> Optional[models.User]:

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
    except JWTError:
        return None

    # Not sure i like just checking the token but it does make testing easier
    # if not user.is_admin:
    if not payload.get("is_admin"):
        raise HTTPException(status_code=401, detail="Admin privileges required")
    return user
