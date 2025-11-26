from __future__ import annotations

from typing import Optional

from pydantic import BaseModel


class ProjectRead(BaseModel):
    id: int
    name: str
    description: Optional[str]

    class Config:
        orm_mode = True
