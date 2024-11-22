from enum import Enum as PyEnum
from sqlalchemy import String, ForeignKey, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class PractitionerType(PyEnum):
    """Practitioner Type Enum"""
    doctor = "doctor"
    nurse = "nurse"
    community_health = "community_health"


class MedicalPractitioner(BaseModel, Base):
    """Medical Practitioner Class"""
    __tablename__ = "medical_practitioners"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    other_names: Mapped[str] = mapped_column(String(60), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(60), nullable=False)
    practitioner_type: Mapped[str] = mapped_column(
        Enum(PractitionerType), nullable=False)
    specialization: Mapped[str] = mapped_column(String(60), nullable=True)
    license_number: Mapped[str] = mapped_column(String(60), nullable=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    availability: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)

    user: Mapped['User'] = relationship(
        back_populates="medical_practitioner", uselist=False)
    medical_histories: Mapped[list['MedicalHistory']] = relationship(
        back_populates="medical_practitioner")
