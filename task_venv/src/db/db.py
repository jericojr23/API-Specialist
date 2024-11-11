import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "dbname=task_db user=postgres password=1234 host=localhost port=5432",
)

# Create a connection pool
db_pool = psycopg2.pool.SimpleConnectionPool(1, 10, DATABASE_URL)


@contextmanager
def get_db_connection():
    conn = db_pool.getconn()
    try:
        yield conn
    finally:
        db_pool.putconn(conn)
