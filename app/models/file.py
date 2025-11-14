from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, func, Boolean
import uuid
from datetime import datetime


class File(Base):

    __tablename__ = "files"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    original_filename: Mapped[str] = mapped_column(String(256), nullable=False)
    stored_filename: Mapped[str] = mapped_column(String(256), nullable=False)
    file_path: Mapped[str] = mapped_column(String(512), nullable=False, unique=True)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)
    extension: Mapped[str] = mapped_column(String(10), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    is_processed: Mapped[bool] = mapped_column(Boolean, default=False)

    user = relationship("User", back_populates="files", lazy="selectin")
    tasks = relationship("Task", back_populates="file", cascade="all, delete-orphan", lazy="selectin")

    __table_args__ = (
        Index('idx_files_user_uploaded', 'user_id', 'uploaded_at'),
        Index('idx_files_processed', 'is_processed'),
    )

