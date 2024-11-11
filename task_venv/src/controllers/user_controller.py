from fastapi import HTTPException, status
import psycopg2
from psycopg2 import sql
from models.user import UserCreate, User
from db.db import DATABASE_URL
from datetime import datetime
from typing import List


from datetime import datetime
from typing import List
import psycopg2
from fastapi import HTTPException, status


def get_all_users() -> List[User]:
    # Get all the users in the database
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username, role, created_at FROM users")
            users = cur.fetchall()

            # Format created_at as a string for each user
            users = [
                User(
                    username=user[0],
                    role=user[1],
                    created_at=user[2].strftime("%Y-%m-%d %H:%M:%S")
                    if user[2]
                    else None,
                )
                for user in users
            ]
            return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def create_user(user_create: UserCreate):
    """Create a new user in the PostgreSQL database."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # Check if user already exists
            cur.execute(
                "SELECT * FROM users WHERE username = %s", (user_create.username,)
            )
            if cur.fetchone():
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username already exists.",
                )

            # Insert the user into the database
            cur.execute(
                """
                INSERT INTO users (username, role, created_at)
                VALUES (%s, %s, %s) RETURNING username, role, created_at
                """,
                (user_create.username, user_create.role, datetime.now()),
            )

            user_data = cur.fetchone()
            conn.commit()

            return User(
                username=user_data[0], role=user_data[1], created_at=user_data[2]
            )

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def get_user_role(username: str) -> str:
    """Retrieve the role of a user from the database."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # Retrieve role of user from database
            cur.execute("SELECT role FROM users WHERE username = %s", (username,))
            user = cur.fetchone()
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )
            return user[0]  # Return the role
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()
