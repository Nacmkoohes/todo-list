from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from todo.db.base import Base
from todo.config import ALLOWED_STATUSES

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="todo")
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="tasks")

    def __repr__(self) -> str:
        return f"<Task #{self.id} {self.title!r} status={self.status!r}>"
