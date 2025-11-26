from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProjectCreate(BaseModel):
    """Schema for creating a new project."""
    name: str = Field(
        ...,
        max_length=200,
        description="Human-readable project name (must be unique).",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Optional longer description of the project.",
    )

    # This is shown as an example in Swagger (OpenAPI)
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Study",
                "description": "Prepare cardiology notes and todo list.",
            }
        }
    )


class ProjectUpdate(BaseModel):
    """Schema for partially updating an existing project."""
    name: Optional[str] = Field(
        None,
        max_length=200,
        description="New name for the project (optional).",
    )
    description: Optional[str] = Field(
        None,
        max_length=1000,
        description="Updated description for the project (optional).",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Study (exam week)",
                "description": "Focus on HF, ACS and arrhythmias before exam.",
            }
        }
    )
