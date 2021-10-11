from fastapi.testclient import TestClient


def test_admin_auth(client: TestClient, admin_auth_header: str) -> None:
    response = client.get("/admin_required/", headers=admin_auth_header)
    assert response.status_code == 200, response.text


def test_admin_auth_forbidden(client: TestClient, auth_header: str) -> None:
    response = client.get("/admin_required/", headers=auth_header)
    assert response.status_code == 401, response.text
