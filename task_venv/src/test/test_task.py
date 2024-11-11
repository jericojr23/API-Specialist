# test_task.py
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_create_task_as_user():
    response = client.post(
        "/create_task/",
        json={
            "title": "Test Task",
            "priority": "Standard",
            "status": "Pending",
            "owner": "user1",
        },
    )
    assert response.status_code == 200
