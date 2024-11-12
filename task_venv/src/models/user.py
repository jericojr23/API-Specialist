from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class User(BaseModel):
    username: str
    role: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    username: str
    role: str

    class Config:
        orm_mode = True
