from app.database.base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy import Boolean, ForeignKey, Index, String, DateTime, func
from datetime import datetime

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    refresh_token: Mapped[str] = mapped_column(String(512), unique=True, nullable=False)
    device_info: Mapped[str] = mapped_column(String(512))
    ip_address: Mapped[str] = mapped_column(String(45))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="refresh_tokens", lazy="select")

    __table_args__ = (
        Index('idx_refresh_tokens_user_active', 'user_id', 'is_active'),  
        Index('idx_refresh_tokens_expires_at', 'expires_at'),  
    )

