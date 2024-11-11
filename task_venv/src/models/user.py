from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    role: str  # Either 'admin' or 'user'


class User(BaseModel):
    username: str
    role: str
    created_at: datetime

    class Config:
        orm_mode = True
