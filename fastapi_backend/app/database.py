from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./bookstore_app.db" # dev db

# Use postgress to make dbdiagram compatible dumps fot db visualization
#SQLALCHEMY_DATABASE_URL = "postgresql://test_user:test_password@127.0.0.1/bookstore_db"

engine = create_engine(         # This is just for sqlite
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
	# Experiment with pool_size later
	#SQLALCHEMY_DATABASE_URL, # pool_size=100, max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
