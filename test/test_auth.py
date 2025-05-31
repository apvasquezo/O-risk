from fastapi.testclient import TestClient
from main import app
client = TestClient(app)

# Credenciales de prueba
USERNAME = "kardam"
PASSWORD = "1234"

def test_login_success():
    response = client.post(
        "/login",
        json={"username": USERNAME, "password": PASSWORD},  #  Enviar como JSON
        headers={"Content-Type": "application/json"}  
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_login_failure():
    response = client.post(
        "/login",
        json={"username": USERNAME, "password": "wrongpassword"},
        headers={"Content-Type": "application/json"}  
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}
