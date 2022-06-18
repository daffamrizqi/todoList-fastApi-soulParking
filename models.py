from enum import Enum
from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID


class Status(str, Enum):
    finished = "Finished"
    on_process = "on Process"


class Todo(BaseModel):
    id: Optional[UUID] = None
    title: str
    description: str
    created_at: Optional[str]
    finished_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
    status: Optional[List[Status]] = Status.on_process


class TodoUpdateReq(BaseModel):
    title: Optional[str]
    description: Optional[str]
    created_at: Optional[str]
    finished_at: Optional[str]
    updated_at: Optional[str]
    deleted_at: Optional[str]
    status: Optional[List[Status]]
