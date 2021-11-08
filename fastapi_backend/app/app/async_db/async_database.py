from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

USER = settings.POSTGRES_USER
PASSWORD = settings.POSTGRES_PASSWORD
SERVER = settings.POSTGRES_SERVER
DB = settings.POSTGRES_DB

DATABASE_URL = f"postgresql+asyncpg://{USER}:{PASSWORD}@{SERVER}/{DB}"

engine = create_async_engine(DATABASE_URL, future=True, echo=True, pool_size=300)

async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
