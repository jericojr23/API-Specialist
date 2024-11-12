from fastapi import HTTPException
from psycopg2 import connect
from models.task import TaskUpdate, TaskResponse
from db.db import DATABASE_URL
from controllers.task import get_role


def update_task_in_db(
    task_id: int, task_update: TaskUpdate, username: str
) -> TaskResponse:
    """Update a task's details in the database and return the updated task."""
    try:
        conn = connect(DATABASE_URL)
        with conn.cursor() as cur:
            # Fetch the current user from the input username
            current_user = get_role(username)

            # Fetch the task's owner to ensure the user is allowed to update
            cur.execute("SELECT owner_id FROM tasks WHERE task_id = %s", (task_id,))
            task = cur.fetchone()

            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            task_owner_id = task[0]

            # Admins can update any task; users can only update tasks they own
            if (
                current_user["role"] != "admin"
                and task_owner_id != current_user["user_id"]
            ):
                raise HTTPException(
                    status_code=403,
                    detail="You are not authorized to update this task",
                )

            # Validate priority value if provided
            valid_priorities = ["Low", "Medium", "High"]
            if task_update.priority and task_update.priority not in valid_priorities:
                raise HTTPException(status_code=400, detail="Invalid priority value")

            # Validate status value if provided
            valid_statuses = ["Pending", "In Progress", "Completed"]
            if task_update.status and task_update.status not in valid_statuses:
                raise HTTPException(status_code=400, detail="Invalid status value")

            # Build the update query dynamically based on the provided fields
            update_fields = []
            parameters = []

            if task_update.title:
                update_fields.append("title = %s")
                parameters.append(task_update.title)

            if task_update.description:
                update_fields.append("description = %s")
                parameters.append(task_update.description)

            if task_update.due_date:
                update_fields.append("due_date = %s")
                parameters.append(task_update.due_date)

            if task_update.priority:
                update_fields.append("priority = %s")
                parameters.append(task_update.priority)

            if task_update.status:
                update_fields.append("status = %s")
                parameters.append(task_update.status)

            # Ensure there is at least one field to update
            if not update_fields:
                raise HTTPException(
                    status_code=400,
                    detail="No fields to update provided",
                )

            # Add the task ID to the parameters list for the WHERE clause
            parameters.append(task_id)

            # Build the SQL query for the update
            update_query = f"""
                UPDATE tasks
                SET {', '.join(update_fields)}
                WHERE task_id = %s
                RETURNING task_id, title, description, due_date, priority, status,
                    (SELECT username FROM users WHERE user_id = owner_id) AS owner,
                    creation_timestamp;
            """

            # Execute the update query
            cur.execute(update_query, tuple(parameters))

            # Commit the transaction to save the changes
            conn.commit()

            # Fetch the updated task
            updated_task = cur.fetchone()

            # If no task was found, raise a 404 error
            if not updated_task:
                raise HTTPException(status_code=404, detail="Task not found")

            # Map the updated task data to the TaskResponse model
            (
                task_id,
                title,
                description,
                due_date,
                priority,
                status,
                owner,
                creation_timestamp,
            ) = updated_task

            # Return the updated task as a response
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

    except Exception as e:
        # Handle any unexpected errors by raising an HTTP exception
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Ensure the connection is closed
        conn.close()
