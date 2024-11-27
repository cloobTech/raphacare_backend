from datetime import datetime
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class Consultation(BaseModel, Base):
    """Consultation Class"""
    __tablename__ = "consultations"

    appointment_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("appointments.id"), nullable=False)
    diagnosis: Mapped[str] = mapped_column(Text, nullable=False)
    follow_up_start_date: Mapped[datetime] = mapped_column(nullable=True)
    follow_up_end_date: Mapped[datetime] = mapped_column(nullable=True)

    appointment: Mapped['Appointment'] = relationship(
        back_populates="consultation",  uselist=False)
    prescription: Mapped['Prescription'] = relationship(
        back_populates="consultation",  uselist=False)
