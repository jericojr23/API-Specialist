# from fastapi import APIRouter, Depends, Header, HTTPException, status
# from models.task import TaskCreate, TaskResponse
# from controllers.task_controllers import (
#     create_task,
#     get_task_by_id,
# )
# from controllers.user_controller import get_user_role

# # API versioning
# router = APIRouter(prefix="/v1/tasks")


# def get_username(x_username: str = Header(...)):
#     # user = get_user_role(x_username)
#     if not x_username:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Username not provided in headers",
#         )
#     return x_username


# @router.post("/create/", response_model=TaskResponse)
# async def create_task_endpoint(task: TaskCreate, username: str = Depends(get_username)):
#     """
#     Create a new task. Admins can create tasks for anyone. Users can create tasks only for themselves.
#     """
#     if task.owner != username and username != "admin":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="You can only create tasks for yourself.",
#         )

#     created_task = create_task(task, username)
#     return created_task


# @router.get("/{task_id}", response_model=TaskResponse)
# async def get_task_endpoint(task_id: int, x_username: str = Depends(get_username)):
#     """Retrieve a task by its ID."""
#     task = get_task_by_id(task_id, x_username)
#     return task
