import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture
def create_admin_account():
    account_data = {"username": "admin", "role": "admin"}

    # Send POST request to create an admin account
    response = client.post("http://127.0.0.1:8000/v1/users/create", json=account_data)

    return response


@pytest.fixture
def create_user_account():
    account_data = {"username": "user", "role": "user"}

    # Send POST request to create a user account
    response = client.post("http://127.0.0.1:8000/v1/users/create", json=account_data)

    return response


def test_create_admin_account(create_admin_account):
    # Check that the response for admin account creation is successful
    response = create_admin_account
    assert response.status_code == 201  # HTTP 201: Created
    assert response.json()["username"] == "admin"
    assert response.json()["role"] == "admin"


def test_create_user_account(create_user_account):
    # Check that the response for user account creation is successful
    response = create_user_account
    assert response.status_code == 201  # HTTP 201: Created
    assert response.json()["username"] == "user"
    assert response.json()["role"] == "user"
