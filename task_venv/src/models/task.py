from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Union, List


# Default task creation model
class TaskCreate(BaseModel):
    title: str = "Empty"
    description: Optional[str] = "Empty"
    due_date: datetime
    priority: str = "Low"
    status: Optional[str] = "Pending"

    class Config:
        orm_mode = True


# Response model for viewing the task
class TaskResponse(BaseModel):
    task_id: int
    title: str
    description: Optional[str]
    due_date: datetime
    priority: str
    status: str
    owner: str
    creation_timestamp: datetime

    class Config:
        orm_mode = True

    # Method to convert datetime fields into string format for serialization
    def dict(self, *args, **kwargs):
        task_dict = super().dict(*args, **kwargs)
        # Convert datetime to ISO string format for response serialization
        if isinstance(task_dict.get("due_date"), datetime):
            task_dict["due_date"] = task_dict["due_date"].isoformat()
        if isinstance(task_dict.get("creation_timestamp"), datetime):
            task_dict["creation_timestamp"] = task_dict[
                "creation_timestamp"
            ].isoformat()
        return task_dict


class TaskListResponse(BaseModel):
    tasks: Union[List[TaskResponse], None] = None
    message: Union[str, None] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None
    status: Optional[str] = None

    class Config:
        orm_mode = True
