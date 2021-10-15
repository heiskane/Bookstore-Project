from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext import asyncio as asyncio_ext
from sqlalchemy.orm import declarative_base  # type: ignore[attr-defined]
from sqlalchemy.orm import sessionmaker, scoped_session

DATABASE_URL = "postgresql+asyncpg://test_user:test_password@db:5432/bookstore_db"

engine = asyncio_ext.create_async_engine(DATABASE_URL, future=True, echo=True)

#Base = declarative_base()
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
#async_session = AsyncSession(engine)
