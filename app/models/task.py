from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import ForeignKey, Index, String, JSON, Text, Integer, Boolean, DateTime, func
from datetime import datetime
from typing import Optional

class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    file_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    celery_task_id: Mapped[str] = mapped_column(String(256), nullable=False, index=True)
    operation_type: Mapped[str] = mapped_column(String(30), nullable=False, index=True)
    
    status: Mapped[str] = mapped_column(
        String(15), 
        nullable=False, 
        index=True,
        default='pending'
    )
    
    parameters: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    result_file_path: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    progress: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime, 
        nullable=False, 
        server_default=func.now()
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    notification_sent: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    user = relationship("User", back_populates="tasks", lazy="selectin")
    file = relationship("File", back_populates="tasks", lazy="selectin")


    __table_args__ = (
        Index('ix_tasks_user_status', 'user_id', 'status'),
        Index('ix_tasks_status_created', 'status', 'created_at'),
        Index('ix_tasks_completed_at', 'completed_at'),
    )






