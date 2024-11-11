# src/services/auth.py

from fastapi import Header, HTTPException, Depends
from typing import Optional

# Define our predefined users and their roles
USERS = {"admin": "admin", "user": "user"}


class User:
    def __init__(self, username: str, role: str):
        self.username = username
        self.role = role


def get_current_user(x_username: Optional[str] = Header(None)) -> User:
    # Check if the username is provided in headers
    if x_username is None:
        raise HTTPException(status_code=401, detail="Username header missing.")

    # Get the user's role
    role = USERS.get(x_username)
    if not role:
        raise HTTPException(status_code=403, detail="User not recognized.")

    # Return a User instance with the username and role
    return User(username=x_username, role=role)


def authorize_admin(user: User):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin users are allowed.")
