from fastapi import HTTPException
from psycopg2 import connect
from db.db import DATABASE_URL
from controllers.task import (
    get_role,
)  # Assuming this function exists and returns the user's role


def delete_task_from_db(task_id: int, username: str) -> str:
    """Delete a task from the database by its task_id, with authorization checks."""
    try:
        # Establish the database connection
        conn = connect(DATABASE_URL)
        with conn.cursor() as cur:
            # Fetch the current user's role and user_id (assuming get_role function returns a dict with role and user_id)
            current_user = get_role(username)
            user_role = current_user["role"]
            user_id = current_user["user_id"]

            # Fetch the task's owner_id to ensure the user has permission to delete it
            cur.execute("SELECT owner_id FROM tasks WHERE task_id = %s", (task_id,))
            task = cur.fetchone()

            if not task:
                raise HTTPException(status_code=404, detail="Task not found")

            task_owner_id = task[0]

            # Admins can delete any task; users can only delete tasks they own
            if user_role != "admin" and task_owner_id != user_id:
                raise HTTPException(
                    status_code=403,  # Forbidden error
                    detail="You are not authorized to delete this task",
                )

            # Define the DELETE SQL query
            delete_query = """
                DELETE FROM tasks
                WHERE task_id = %s
                RETURNING task_id;
            """

            # Execute the DELETE query
            cur.execute(delete_query, (task_id,))
            deleted_task = cur.fetchone()

            # If no task is deleted, raise a 404 error
            if not deleted_task:
                raise HTTPException(status_code=404, detail="Task not found")

            # Commit the transaction
            conn.commit()

            # Return a success message
            return f"Task {task_id} deleted successfully"

    except Exception as e:
        # Handle any unexpected errors by raising an HTTP exception
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

    finally:
        # Ensure the connection is closed
        conn.close()
