from fastapi import HTTPException, status
import psycopg2
from psycopg2 import sql
from models.user import UserCreate, User
from db.db import DATABASE_URL
from datetime import datetime
from typing import List


def get_all_users() -> List[User]:
    # Get all the users in the database
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT username, role, created_at FROM users")
            users = cur.fetchall()
            # Return the list of users
            users = [
                User(username=user[0], role=user[1], created_at=[2]) for user in users
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
