from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str

class TaskCreate(TaskBase):
    assigned_to_emp_id: str

class TaskResponse(TaskBase):
    id: UUID
    status: str
    assigned_by: UUID
    assigned_to: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    status: Optional[str] = None
