from fastapi import HTTPException, status, Header
from models.task import TaskCreate, TaskResponse, TaskListResponse
from datetime import datetime
import psycopg2
from db.db import DATABASE_URL
from models.user import User
from typing import Optional


def create_task(task: TaskCreate, username: str) -> TaskResponse:
    """Create a new task."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        # Checks first the role of the user
        user = get_role(username)
        if user["role"] != "admin" and username != username:
            raise HTTPException(
                status_code=403,
                detail="Unauthorized to create tasks",
            )

        with conn.cursor() as cur:
            # Insert task into database, using the provided status or default if not specified
            cur.execute(
                """
                INSERT INTO tasks (title, description, due_date, priority, owner_id, status)
                VALUES (%s, %s, %s, %s, (SELECT user_id FROM users WHERE username = %s), %s)
                RETURNING task_id, title, description, due_date, priority, status, owner_id, creation_timestamp 
                """,
                (
                    task.title,
                    task.description,
                    task.due_date,
                    task.priority,
                    username,
                    task.status,
                ),
            )

            # Fetch the created task details
            (
                task_id,
                title,
                description,
                due_date,
                priority,
                status,
                owner_id,
                creation_timestamp,
            ) = cur.fetchone()
            conn.commit()

            # Return the created task as a response
            task_response = TaskResponse(
                task_id=task_id,
                title=title,
                description=description,
                due_date=due_date,
                priority=priority,
                status=status,
                owner=username,
                creation_timestamp=creation_timestamp,
            )

            print(task_response)
            return task_response

    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=str(e),
        )
    finally:
        conn.close()


def get_username(x_username: Optional[str] = Header(None)) -> str:
    # Get the username from the x-username header
    if x_username is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Username not provided"
        )
    return x_username


def get_role(username: str):
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # Fetch user information including user_id
            cur.execute(
                "SELECT user_id, username, role FROM users WHERE username = %s",
                (username,),
            )
            user = cur.fetchone()

            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "user_id": user[0],
                "username": user[1],
                "role": user[2],
            }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def get_all_tasks() -> list[TaskResponse]:
    """Retrieve all tasks from the database."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # Retrieve all tasks from the database
            cur.execute("""
                SELECT task_id, title, description, due_date, priority, status, 
                (SELECT username FROM users WHERE user_id = owner_id) AS owner, 
                creation_timestamp
                FROM tasks
            """)
            tasks = cur.fetchall()

            # If no tasks found, raise a 404 error
            if not tasks:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No tasks found"
                )

            # Map the result to TaskResponse models
            task_list = [
                TaskResponse(
                    task_id=task_id,
                    title=title,
                    description=description,
                    due_date=due_date,
                    priority=priority,
                    status=status,
                    owner=owner,
                    creation_timestamp=creation_timestamp,
                )
                for task_id, title, description, due_date, priority, status, owner, creation_timestamp in tasks
            ]

            return task_list

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()


def get_filtered_tasks(
    due_date: str = None, priority: str = None, status: str = None
) -> TaskListResponse:
    """Retrieve tasks from the database with optional filtering by due date, priority, or status."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        # Prepare the SQL query with filters
        conditions = []
        parameters = []

        if due_date:
            conditions.append("due_date = %s")
            parameters.append(due_date)

        if priority:
            conditions.append("priority = %s")
            parameters.append(priority)

        if status:
            conditions.append("status = %s")
            parameters.append(status)

        # Build the WHERE clause dynamically based on filters
        where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

        query = f"""
            SELECT task_id, title, description, due_date, priority, status,
            (SELECT username FROM users WHERE user_id = owner_id) AS owner,
            creation_timestamp
            FROM tasks
            {where_clause}
        """

        with conn.cursor() as cur:
            cur.execute(query, tuple(parameters))
            tasks = cur.fetchall()

            # If no tasks found, return a custom message inside TaskListResponse
            if not tasks:
                return TaskListResponse(
                    tasks=[],  # No tasks found, return an empty list
                    message="No existing tasks found",
                )

            # Map the result to TaskResponse models
            task_list = [
                TaskResponse(
                    task_id=task_id,
                    title=title,
                    description=description,
                    due_date=due_date,
                    priority=priority,
                    status=status,
                    owner=owner,
                    creation_timestamp=creation_timestamp,
                )
                for task_id, title, description, due_date, priority, status, owner, creation_timestamp in tasks
            ]

            # Return the response wrapped in TaskListResponse
            return TaskListResponse(
                tasks=task_list,  # List of TaskResponse models
                message=None,  # Optional message can be None when there are tasks
            )

    except Exception as e:
        # Handle any unexpected errors gracefully
        raise HTTPException(detail=str(e))
    finally:
        conn.close()


def get_task_by_id(task_id: int, username: str) -> TaskResponse:
    """Retrieve a specific task by its ID, checking if the user is the owner or an admin."""
    conn = psycopg2.connect(DATABASE_URL)
    try:
        with conn.cursor() as cur:
            # Fetch task details
            cur.execute(
                "SELECT task_id, title, description, due_date, priority, status, owner_id, creation_timestamp "
                "FROM tasks WHERE task_id = %s",
                (task_id,),
            )
            task = cur.fetchone()

            if not task:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
                )

            (
                task_id,
                title,
                description,
                due_date,
                priority,
                status,
                owner_id,
                creation_timestamp,
            ) = task

            # Set status to 'Pending' if None
            if status is None:
                status = "Pending"

            # Fetch user role and user_id for validation
            cur.execute(
                "SELECT user_id, role FROM users WHERE username = %s", (username,)
            )
            user = cur.fetchone()

            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
                )

            user_id = user[0]
            user_role = user[1]

            # Check if the user is an admin or the owner of the task
            if user_role == "admin" or user_id == owner_id:
                # User is authorized, return the task
                owner = username if owner_id else None
                return TaskResponse(
                    task_id=task_id,
                    title=title,
                    description=description,
                    due_date=due_date,
                    priority=priority,
                    status=status,
                    owner=owner,
                    creation_timestamp=creation_timestamp,
                )

            # If the user is neither the owner nor an admin, deny access
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own tasks.",
            )
    except HTTPException as e:
        raise e  # Reraise any HTTPException to return the proper status code
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    finally:
        conn.close()
