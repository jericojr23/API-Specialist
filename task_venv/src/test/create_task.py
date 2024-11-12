import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def create_task_data():
    return {
        "title": "Test Task",
        "description": "Test task description",
        "due_date": "2024-11-12",
        "priority": "Low",
        "status": "In Progress",
    }


def test_create_task_as_admin(create_task_data):
    headers = {"x-username": "admin"}  # Admin can create tasks for anyone

    # Create a task as admin
    response = client.post(
        "http://127.0.0.1:8000/v1/tasks/create", json=create_task_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == create_task_data["title"]
    assert response.json()["owner"] == "admin"  # The owner should be admin


def test_create_task_as_user(create_task_data):
    headers = {"x-username": "user"}  # User can only assign task to themselves

    # Create a task as user
    response = client.post(
        "http://127.0.0.1:8000/v1/tasks/create", json=create_task_data, headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == create_task_data["title"]
    assert response.json()["owner"] == "user"  # The owner should be user


def test_create_task_without_username(create_task_data):
    # Try to create a task without providing the 'x-username' header (should be unauthorized)
    response = client.post(
        "http://127.0.0.1:8000/v1/tasks/create", json=create_task_data
    )
    assert response.status_code == 401  # Unauthorized
