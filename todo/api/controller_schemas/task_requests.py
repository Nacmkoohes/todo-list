from __future__ import annotations

from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class TaskCreate(BaseModel):
    """Schema for creating a new task inside a project."""

    title: str = Field(
        ...,
        max_length=200,
        description="Short title describing the task.",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional longer text explaining the task details.",
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Optional deadline in ISO 8601 format (UTC recommended).",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Write cardiology summary",
                "description": "Summarize HF, ACS, arrhythmias for tomorrow’s session.",
                "deadline": "2025-12-01T18:00:00Z",
            }
        }
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task (partial update)."""

    title: Optional[str] = Field(
        None,
        max_length=200,
        description="Updated title for the task.",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Updated task description.",
    )
    status: Optional[str] = Field(
        None,
        description="Updated status (allowed values: todo, doing, done).",
    )
    deadline: Optional[datetime] = Field(
        None,
        description="Updated deadline in ISO format.",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Prepare slides for API project",
                "description": "Add diagrams for API architecture and services.",
                "status": "doing",
                "deadline": "2025-12-02T16:00:00Z",
            }
        }
    )
