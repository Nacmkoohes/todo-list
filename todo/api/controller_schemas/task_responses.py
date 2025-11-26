from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TaskRead(BaseModel):
    """Response model returned when reading a task."""

    id: int = Field(..., description="Unique identifier for the task.")
    project_id: int = Field(..., description="ID of the project this task belongs to.")
    title: str = Field(..., description="Task title.")
    description: Optional[str] = Field(
        None,
        description="Optional detailed description of the task.",
    )
    status: str = Field(
        ...,
        description="Current status of the task (todo, doing, done).",
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Deadline of the task in ISO 8601 format.",
    )
    closed_at: Optional[datetime] = Field(
        None,
        description="Timestamp when the task was automatically or manually closed.",
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 12,
                "project_id": 3,
                "title": "Prepare API documentation",
                "description": "Add examples and polish request/response schemas.",
                "status": "doing",
                "deadline": "2025-12-03T14:00:00Z",
                "closed_at": None,
            }
        },
    )
