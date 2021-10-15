from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://test_user:test_password@db:5432/bookstore_db"

engine = create_async_engine(DATABASE_URL, future=True, echo=True, pool_size=50)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
