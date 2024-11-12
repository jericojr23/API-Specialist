import psycopg2
import sys
import os

# Add the src directory to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.db import DATABASE_URL  # Now this should work


# Define your schema
TASKS_TABLE_SCHEMA = """
CREATE TABLE tasks (
    task_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    due_date DATE NOT NULL,
    priority VARCHAR(10) CHECK (priority IN ('Low', 'Medium', 'High')),
    status VARCHAR(20) CHECK (status IN ('Pending', 'In Progress', 'Completed')),
    owner_id INT NOT NULL,
    creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users (user_id) ON DELETE CASCADE
);
"""

USERS_TABLE_SCHEMA = """
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    role VARCHAR(10) CHECK (role IN ('admin', 'user')) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
"""


def initialize_database():
    conn = None
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(DATABASE_URL)
        with conn.cursor() as cur:
            # Drop the existing tables if they exist
            cur.execute("DROP TABLE IF EXISTS tasks;")
            cur.execute("DROP TABLE IF EXISTS users;")

            # Execute table creation statements
            cur.execute(USERS_TABLE_SCHEMA)
            cur.execute(TASKS_TABLE_SCHEMA)

            # Commit the changes
            conn.commit()
            print("Database tables recreated successfully.")
    except Exception as e:
        print("An error occurred while initializing the database:", e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    initialize_database()
