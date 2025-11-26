from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class TaskRead(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: str
    deadline: Optional[datetime]
    closed_at: Optional[datetime]

    class Config:
        orm_mode = True
