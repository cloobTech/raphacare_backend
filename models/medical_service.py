from enum import Enum as PyEnum
from sqlalchemy import ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class ServiceApprovalStatus(PyEnum):
    """Service Status Enum"""
    pending = "pending"
    approved = "approved"
    declined = "declined"


class Service(BaseModel, Base):
    """Service Class"""
    __tablename__ = 'services'

    name: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(nullable=False, default=0.0)
    medical_practitioner_id: Mapped[str] = mapped_column(
        ForeignKey('medical_practitioners.id'), nullable=True)
    admin_id: Mapped[str] = mapped_column(
        ForeignKey('admins.id'), nullable=True)
    is_admin_defined: Mapped[bool] = mapped_column(
        nullable=False, default=False)
    approval_status: Mapped[str] = mapped_column(
        Enum(ServiceApprovalStatus), nullable=False, default=ServiceApprovalStatus.pending)

    medical_practitioner: Mapped['MedicalPractitioner'] = relationship(
        back_populates='services', uselist=False)
    admin: Mapped['Admin'] = relationship(
        back_populates='services', uselist=False)
