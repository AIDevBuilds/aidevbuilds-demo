from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from uuid import UUID


class Priority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class UserInDB(BaseModel):
    username: str
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class TaskCreate(BaseModel):
    title: str
    description: str
    priority: Priority


class Task(BaseModel):
    id: UUID
    title: str
    description: str
    priority: Priority
    created_at: datetime
    owner_username: str
