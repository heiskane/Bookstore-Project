from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..app.database import Base
from ..app.main import app, get_db

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


def test_create_book():
	response = client.post(
		"/books/",
		json = {
		  "authors": [
		    {"name": "Test author1"}, {"name": "Test author2"}],
		  "book": {
		    "title": "Test Book",
		    "description": "string",
		    "language": "string",
		    "price": 0,
		    "publication_date": "2021-09-05",
		    "isbn": "string",
		    "genres": [
		      "string"
		    ]}}
	)
	assert response.status_code == 200, response.text
	data = response.json()
	assert data["title"] == "Test Book"


def test_get_book():
	response = client.get(
		"/books/1"
	)
	assert response.status_code == 200, response.text
	data = response.json()
	assert data["title"] == "Test Book"
	assert data["authors"][0]["name"] == "Test author1"
	assert data["authors"][1]["name"] == "Test author2"
