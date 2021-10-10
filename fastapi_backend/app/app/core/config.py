from typing import Optional
from pydantic import BaseSettings, PostgresDsn

# https://pydantic-docs.helpmanual.io/usage/settings/
# https://github.com/tiangolo/full-stack-fastapi-postgresql/blob/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app/core/config.py
class Settings(BaseSettings):
	"""Tries to read environment variables to set the settings"""
	SECRET_KEY: str

	# 60 minutes * 24 hours * 8 days = 8 days
	ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

	POSTGRES_SERVER: str
	POSTGRES_USER: str
	POSTGRES_PASSWORD: str
	POSTGRES_DB: str
	SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

settings = Settings()