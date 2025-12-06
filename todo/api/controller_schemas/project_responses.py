from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class ProjectRead(BaseModel):
    """Response schema returned when reading a project."""

    id: int = Field(..., description="Unique identifier of the project.")
    name: str = Field(..., description="Human-readable project name.")
    description: Optional[str] = Field(
        None,
        description="Optional longer description of the project.",
    )

    # Pydantic v2 config
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "name": "Study",
                "description": "Prepare cardiology notes and todo items.",
            }
        },
    )
