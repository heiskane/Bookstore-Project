from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from starlette.config import environ

# Not the most elegant solution but it will have to do
#if environ["TESTING"] == "True":
#	SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
#	engine = create_engine(SQLALCHEMY_DATABASE_URL)
#
#else:
SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@db/bookstore_db"

engine = create_engine(
	# Experiment with pool_size later
	SQLALCHEMY_DATABASE_URL, pool_size=100, max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
