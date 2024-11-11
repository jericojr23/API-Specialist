import psycopg2
from psycopg2 import sql
from db import DATABASE_URL

# Define your schema
TASKS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    priority VARCHAR(10) CHECK (priority IN ('Low', 'Medium', 'High')),
    status VARCHAR(20) CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    owner VARCHAR(50) NOT NULL,
    creation_timestamp TIMESTAMP DEFAULT NOW()
);
"""

USERS_TABLE_SCHEMA = """
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    role VARCHAR(10) CHECK (role IN ('admin', 'user')) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
"""


def initialize_database():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            # Drop the existing tables
            cur.execute("DROP TABLE IF EXISTS users;")
            cur.execute("DROP TABLE IF EXISTS tasks;")
            # Execute table creation statements
            cur.execute(TASKS_TABLE_SCHEMA)
            cur.execute(USERS_TABLE_SCHEMA)
            conn.commit()
            print("Database tables recreated successfully.")
    except Exception as e:
        print("An error occurred while initializing the database:", e)
    finally:
        conn.close()


if __name__ == "__main__":
    initialize_database()
