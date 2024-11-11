# models/task.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TaskCreate(BaseModel):
    title: str
    description: str
    due_date: datetime
    priority: str


class TaskResponse(TaskCreate):
    task_id: int
    owner: str
    status: str
    creation_timestamp: datetime

    class Config:
        orm_mode = True
