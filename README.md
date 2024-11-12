# Task Management API

This is a Task Management RESTful API built using **FastAPI** with role-based authorization and PostgreSQL for task storage. It supports managing tasks with CRUD operations and implements role-based authorization for users (Admin and User roles). The application is designed to demonstrate core Python fundamentals, object-oriented programming (OOP) principles, and API development with FastAPI.

## Features

- **Admin Role**: Can create, retrieve, update, and delete any task.
- **User Role**: Can create tasks, retrieve their own tasks, and update or delete their own tasks.
- **Task Management**:
  - Create a new task
  - Retrieve all tasks with optional filtering (by due date, priority, or status)
  - Retrieve a specific task by its ID
  - Update a task’s details
  - Mark a task as completed
  - Delete a task
- Role-based authorization using predefined users (`admin` and `user`).
  
## Technologies Used

- **FastAPI**: For building the RESTful API.
- **PostgreSQL**: For task data storage.
- **psycopg2**: Python library for PostgreSQL database connection.
- **Pydantic**: For data validation and serialization.

## Installation

### Prerequisites

- Python 3.x
- PostgreSQL (running locally or on a cloud service)
- pip (Python package installer)

### Steps

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/task-management-api.git
    cd task-management-api
    ```

2. Create a virtual environment and activate it:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up PostgreSQL:
    - Create a new PostgreSQL database (e.g., `task_db`).
    - Run the SQL scripts to create the `tasks` and `users` tables. The script is located at test/db_setup.py
    - Make sure the database credentials are updated in the `DATABASE_URL` string.

    Example SQL to create tables:
    ```sql
    CREATE TABLE tasks (
        task_id SERIAL PRIMARY KEY,
        title VARCHAR(255),
        description TEXT,
        due_date TIMESTAMP,
        priority VARCHAR(50),
        status VARCHAR(50),
        creation_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        owner VARCHAR(255)
    );

    CREATE TABLE users (
        username VARCHAR(255) PRIMARY KEY,
        role VARCHAR(50)
    );
    ```

5. Run the application:
    ```bash
    uvicorn main:app --reload
    ```

    The API will be available at `http://127.0.0.1:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation using **Swagger UI** and **ReDoc**. You can access it at the following endpoints:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## Predefined Users

For testing, you can use the following predefined users to simulate authentication:

- **Admin User**:
  - Username: `admin`
  - Role: `admin`
- **Regular User**:
  - Username: `user`
  - Role: `user`

Use the `X-Username` header to authenticate the user. For example:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/tasks/' \
  -H 'X-Username: admin' \
  -d '{
  "title": "New Task",
  "description": "Task description",
  "due_date": "2024-11-30T00:00:00",
  "priority": "High",
  "status": "Pending"
}'
