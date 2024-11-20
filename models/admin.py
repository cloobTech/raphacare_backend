from enum import Enum as pyEnum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class AdminType(pyEnum):
    """Admin Type Enum"""
    SUPER = "super"
    NORMAL = "normal"


class Admin(BaseModel, Base):
    """Admin class"""
    __tablename__ = "admins"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    type: Mapped[str] = mapped_column(
        Enum(AdminType), nullable=False, default=AdminType.NORMAL)

    user: Mapped['User'] = relationship(
        back_populates="admin", uselist=False)
