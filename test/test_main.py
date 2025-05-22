from fastapi.testclient import TestClient
from main import create_app

client = TestClient(create_app())

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Gestionando Riesgos"}
