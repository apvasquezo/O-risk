from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# Credenciales de prueba
USERNAME = "user1"
PASSWORD = "password1"

def test_login_success():
    response = client.post(
        "/login",
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure():
    response = client.post(
        "/login",
        data={"username": USERNAME, "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_protected_route():
    # Obtener el token de acceso
    token_response = client.post(
        "/login",
        data={"username": USERNAME, "password": PASSWORD},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert token_response.status_code == 200
    token = token_response.json()["access_token"]

    # Acceder a la ruta protegida
    response = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"username": USERNAME}
