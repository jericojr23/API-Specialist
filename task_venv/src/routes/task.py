from controllers.task import (
    create_task,
    get_role,
    get_username,
    get_task_by_id,
    get_all_tasks,
    get_filtered_tasks,
)
from controllers.user import get_user_role
from fastapi import APIRouter, Depends, Header, HTTPException, status, Query
from models.task import TaskCreate, TaskResponse, TaskListResponse, TaskUpdate
from typing import List, Optional
from controllers.task_update import update_task_in_db
from controllers.task_delete import delete_task_from_db

# API versioning
task_router = APIRouter(prefix="/v1/tasks")


@task_router.get("/test")
async def test_route():
    return {"message": "Test route working!"}


@task_router.post("/create", response_model=TaskResponse)
async def create_task_endpoint(task: TaskCreate, username: str = Depends(get_username)):
    """
    Creates a new task.
    Admins can create tasks for anyone.
    Users can create tasks only for themselves.
    """
    current_user = get_role(username)

    # Permission check
    if current_user["role"] != "admin" and username != current_user["username"]:
        raise HTTPException(
            status_code=403,
            detail="You are not authorized to create tasks for this user.",
        )

    try:
        created_task = create_task(task, current_user["username"])

        if created_task is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to create task",
            )

        return created_task

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@task_router.get(
    "/view", response_model=TaskListResponse, response_description="List of all tasks"
)
def view_tasks(
    due_date: Optional[str] = Query(
        None, title="Due Date Filter", description="Filter by due date"
    ),
    priority: Optional[str] = Query(
        None, title="Priority Filter", description="Filter by priority"
    ),
    status: Optional[str] = Query(
        None, title="Status Filter", description="Filter by status"
    ),
):
    """Retrieve tasks with optional filters for due date, priority, and status."""
    try:
        # Call the filtered task retrieval function
        tasks = get_filtered_tasks(due_date=due_date, priority=priority, status=status)
        return tasks  # Return the TaskListResponse directly
    except HTTPException as e:
        raise e


@task_router.get("/{task_id}", response_model=TaskResponse)
async def get_task_by_id_endpoint(
    task_id: int, username: str = Depends(get_username)
) -> TaskResponse:
    """Retrieve a specific task by its ID."""
    try:
        task = get_task_by_id(
            task_id, username
        )  # Retrieve task using the modified logic
        return task
    except HTTPException as e:
        raise e  # Re-raise any HTTPException raised in the service function
    except Exception as e:
        # Return a custom error message if an exception occurs
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="You are not authorized.",
        )


@task_router.put(
    "/update/{task_id}",
    response_model=TaskResponse,
    response_description="Update task details",
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    username: str = Depends(get_username),  # Ensure this correctly gets the username
):
    """Route handler to update a task's details."""
    updated_task = update_task_in_db(
        task_id=task_id, task_update=task_update, username=username
    )
    return updated_task


@task_router.delete(
    "/delete/{task_id}",
    response_description="Delete a task",
)
def delete_task(
    task_id: int,
    username: str = Depends(get_username),  # Ensure this gets the correct username
):
    """Route handler to delete a task by its task_id."""
    try:
        result = delete_task_from_db(task_id=task_id, username=username)
        return {"detail": result}
    except HTTPException as e:
        raise e
