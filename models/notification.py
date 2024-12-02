from enum import Enum as PyEnum
from sqlalchemy import String, ForeignKey, Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class NotificationType(str, PyEnum):
    """Notification Type Enum"""
    appointment = "appointment"
    payment = "payment"


class Notification(BaseModel, Base):
    """Notification Class"""
    __tablename__ = "notifications"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    notification_type: Mapped[str] = mapped_column(
        Enum(NotificationType), nullable=False)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    is_read: Mapped[bool] = mapped_column(nullable=False, default=False)
    resource_id: Mapped[str] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship(
        back_populates="notifications", lazy="selectin", uselist=False)
