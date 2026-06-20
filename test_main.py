from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_root_endpoint():
	response = client.get("/")
	assert response.status_code == 200
	data = response.json()
	assert "message" in data
	assert data ["message"] == "Hello world"

def test_health_endpoint():
	response = client.get("/health")
	assert response.status_code == 200
	data =response.json()
	assert "status" in data
	assert data ["status"] == "alive"
