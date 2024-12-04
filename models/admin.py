from enum import Enum as pyEnum
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class AdminType(str, pyEnum):
    """Admin Type Enum"""
    super = "super"
    normal = "normal"


class Admin(BaseModel, Base):
    """Admin class"""
    __tablename__ = "admins"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    other_names: Mapped[str] = mapped_column(String(60), nullable=True)
    type: Mapped[str] = mapped_column(
        Enum(AdminType), nullable=False, default=AdminType.normal)

    user: Mapped['User'] = relationship(
        back_populates="admin", lazy="joined", uselist=False)
    services: Mapped[list['Service']] = relationship(
        "Service", back_populates="admin")
