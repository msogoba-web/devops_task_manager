import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, engine

client = TestClient(app)

def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

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
    client.post(
        "/tasks",
        json={"id": 1, "title": "Learn DevOps", "completed": False}
    )

    response = client.get("/tasks")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 1

def test_get_task_by_id():
    client.post(
        "/tasks",
        json={"id": 2, "title": "Learn Docker", "completed": False}
    )

    response = client.get("/tasks/2")

    assert response.status_code == 200
    assert response.json()["title"] == "Learn Docker"

def test_delete_task():
    client.post(
        "/tasks",
        json={"id": 3, "title": "Learn Kubernetes", "completed": False}
    )

    response = client.delete("/tasks/3")

    assert response.status_code == 200
    assert response.json() == {"message": "Task deleted"}