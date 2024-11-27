from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, ForeignKey,  Enum, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class AppointmentStatus(str, PyEnum):
    """Appointment Status Enum"""
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"
    completed = "completed"


class AppointmentType(str, PyEnum):
    """Appointment Type Class"""
    online = "online"
    physical = "physical"
    home_service = "home_service"


class Appointment(BaseModel, Base):
    """Appointment Class"""
    __tablename__ = "appointments"

    patient_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("patients.id"), nullable=False)
    medical_practitioner_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("medical_practitioners.id"), nullable=False)
    appointment_start_time: Mapped[datetime] = mapped_column(nullable=False)
    appointment_end_time: Mapped[datetime] = mapped_column(nullable=False)
    appointment_status: Mapped[str] = mapped_column(
        Enum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)
    appointment_type: Mapped[str] = mapped_column(
        Enum(AppointmentType), default=AppointmentType.online, nullable=False)
    appointment_reason: Mapped[str] = mapped_column(Text, nullable=False)
    appointment_note: Mapped[str] = mapped_column(Text, nullable=True)

    patient: Mapped['Patient'] = relationship(
        back_populates="appointments",  uselist=False)
    medical_practitioner: Mapped['MedicalPractitioner'] = relationship(
        back_populates="appointments",  uselist=False)
