from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from ..database import Base
from ..main import app, get_db

# Not sure if i will have time to implement all proper tests

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"


engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Drop all existing data first
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
	try:
		db = TestingSessionLocal()
		yield db
	finally:
		db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_author():
	response = client.post(
		"/authors/",
		json={"name": "Bob"}
	)
	assert response.status_code == 200, response.text
	data = response.json()
	assert data["name"] == "Bob"
	assert "id" in data
	author_id = data["id"]

	response = client.get(f"/authors/{author_id}")
	assert response.status_code == 200, response.text
	data = response.json()
	assert data["name"] == "Bob"
	author_id = data["id"]


def test_create_user():
	response = client.post(
		"/users/",
		json={"username": "test_user", "password": "test_password"}
	)
	assert response.status_code == 200, response.text
	data = response.json()
	assert data["username"] == "test_user"

	response = client.post(
		"/users/",
		json={"username": "Test_User", "password": "test_password"}
	)
	assert response.status_code == 400, response.text
	data = response.json()
	assert data["detail"] == "Username taken"


def test_login():
	response = client.post(
		"/login/",
		data={"username": "test_user", "password": "test_password"}
	)
	assert response.status_code == 200, response.text
	data = response.json()
	access_token = data["access_token"]

	response = client.get(
		"/auth_required/",
		headers={'Authorization': f'Bearer {access_token}'}
	)
	assert response.status_code == 200, response.text

	response = client.get(
		"auth_required"
	)
	assert response.status_code == 401, response.text


	# Only drops all it tests are successfull unfortunately
def finish():
	Base.metadata.drop_all(bind=engine)