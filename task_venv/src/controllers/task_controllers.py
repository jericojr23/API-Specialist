# # controllers/task_controller.py
# from fastapi import HTTPException, status
# from models.task import TaskCreate, TaskResponse
# from models.user import PREDEFINED_USERS
# from datetime import datetime
# import psycopg2
# from db.db import DATABASE_URL


# class Task:
#     def __init__(
#         self,
#         task_id,
#         title,
#         description,
#         due_date,
#         priority,
#         status,
#         owner,
#         creation_timestamp,
#     ):
#         self.task_id = task_id
#         self.title = title
#         self.description = description
#         self.due_date = due_date
#         self.priority = priority
#         self.status = status
#         self.owner = owner
#         self.creation_timestamp = creation_timestamp


# def create_task(task: TaskCreate, username: str) -> TaskResponse:
#     """Create a new task."""
#     conn = psycopg2.connect(DATABASE_URL)
#     try:
#         with conn.cursor() as cur:
#             # Insert task into database
#             cur.execute(
#                 """
#                 INSERT INTO tasks (title, description, due_date, priority, status, owner)
#                 VALUES (%s, %s, %s, %s, 'Pending', %s) RETURNING task_id, creation_timestamp
#                 """,
#                 (task.title, task.description, task.due_date, task.priority, username),
#             )

#             task_id, creation_timestamp = cur.fetchone()
#             conn.commit()

#             # Return the created task
#             return TaskResponse(
#                 task_id=task_id,
#                 title=task.title,
#                 description=task.description,
#                 due_date=task.due_date,
#                 priority=task.priority,
#                 status="Pending",
#                 owner=username,
#                 creation_timestamp=creation_timestamp,
#             )
#     except Exception as e:
#         conn.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
#         )
#     finally:
#         conn.close()


# def get_task_by_id(task_id: int, username: str) -> TaskResponse:
#     """Retrieve a specific task by its ID, checking if the user is the owner."""
#     conn = psycopg2.connect(DATABASE_URL)
#     try:
#         with conn.cursor() as cur:
#             cur.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
#             task = cur.fetchone()
#             if not task:
#                 raise HTTPException(
#                     status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
#                 )

#             (
#                 task_id,
#                 title,
#                 description,
#                 due_date,
#                 priority,
#                 status,
#                 owner,
#                 creation_timestamp,
#             ) = task

#             # Check if user is authorized to view the task
#             if owner != username and PREDEFINED_USERS[username].role != "admin":
#                 raise HTTPException(
#                     status_code=status.HTTP_403_FORBIDDEN,
#                     detail="You can only view your own tasks.",
#                 )

#             return TaskResponse(
#                 task_id=task_id,
#                 title=title,
#                 description=description,
#                 due_date=due_date,
#                 priority=priority,
#                 status=status,
#                 owner=owner,
#                 creation_timestamp=creation_timestamp,
#             )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
#         )
#     finally:
#         conn.close()
