from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_task():
    response = client.post(
        "/tasks",
        json={"id": 1, "title": "Learn DevOps", "completed": False}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Learn DevOps"

def test_get_tasks():
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)