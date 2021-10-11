from datetime import datetime
from datetime import timedelta
from typing import Dict
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from jose import jwt
from pytest import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models

# from pytest import Session
from app.api.deps import get_db
from app.core.config import settings
from app.crud import pwd_context
from app.database import Base
from app.main import app

# Not sure if i will have time to implement all proper tests

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Drop all existing data first
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator:
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="module")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


# Create a user for auth testing
def pytest_sessionstart(session: Session) -> None:
    password_hash = pwd_context.hash("test_password")
    db_user = models.User(
        username="auth_test_user",
        password_hash=password_hash,
        is_active=True,
        is_admin=True,
        register_date=datetime.today(),
    )
    db = TestingSessionLocal()
    db.add(db_user)
    db.commit()


@pytest.fixture(scope="module")
def admin_auth_header() -> Dict[str, str]:
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode = {
        "exp": expire,
        "sub": "auth_test_user",
        "is_admin": True,
        "is_active": True,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {encoded_jwt}"}


@pytest.fixture(scope="module")
def auth_header() -> Dict[str, str]:
    expire = datetime.utcnow() + timedelta(minutes=60)
    to_encode = {
        "exp": expire,
        "sub": "auth_test_user",
        "is_admin": False,
        "is_active": True,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return {"Authorization": f"Bearer {encoded_jwt}"}
