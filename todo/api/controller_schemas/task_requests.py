from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(..., max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    deadline: Optional[datetime] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)
    status: Optional[str] = Field(None)
    deadline: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example": {
                "title": "Fix API bug",
                "description": "Correct failing PUT endpoint",
                "status": "doing",
                "deadline": "2025-12-01T12:00:00Z",
            }
        }
