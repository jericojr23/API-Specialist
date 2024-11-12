import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# Test for retrieving task by ID (assuming task_id = 1 exists)
def test_get_task_by_id_admin():
    task_id = 1  # Task ID is always 1
    headers = {
        "x-username": "admin"
    }  # Simulating the header with the username of 'user'

    # Simulate a GET request to the endpoint to retrieve the task by ID
    response = client.get(f"http://127.0.0.1:8000/v1/tasks/{task_id}", headers=headers)

    # Assert the response status code is 200 OK
    assert response.status_code == 200


def test_get_task_by_id_user():
    task_id = 1  # Task ID is always 1
    headers = {
        "x-username": "user"
    }  # Simulating the header with the username of 'user'

    # Simulate a GET request to the endpoint to retrieve the task by ID
    response = client.get(f"http://127.0.0.1:8000/v1/tasks/{task_id}", headers=headers)

    # Assert the response status code is 200 OK
    assert response.status_code == 200
