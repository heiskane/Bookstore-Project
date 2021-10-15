from fastapi.testclient import TestClient


def test_create_user(client: TestClient) -> None:
    response = client.post(
        "/users/", json={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["access_token"]
    assert data["token_type"] == "bearer"

    response = client.post(
        "/users/", json={"username": "Test_User", "password": "test_password"}
    )
    assert response.status_code == 400, response.text


def test_failed_login(client: TestClient) -> None:
    response = client.post(
        "/login/", data={"username": "wrong_user", "password": "wrong_password"}
    )
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Login failed"


def test_login(client: TestClient) -> None:
    response = client.post(
        "/login/", data={"username": "test_user", "password": "test_password"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    access_token = data["access_token"]

    response = client.get(
        "/auth_required/", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert response.status_code == 200, response.text

    response = client.get("auth_required")
    assert response.status_code == 401, response.text


def test_find_user_by_name(client: TestClient) -> None:
    response = client.get("/users/test_user")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "test_user"
    assert data["is_active"]


def test_list_users(client: TestClient) -> None:
    response = client.get("/users")
    assert response.status_code == 200, response.text
