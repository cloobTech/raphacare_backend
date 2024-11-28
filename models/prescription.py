from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class Prescription(BaseModel, Base):
    """Prescription Class"""
    __tablename__ = "prescriptions"

    consultation_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("consultations.id"), nullable=False)
    medicine_name: Mapped[str] = mapped_column(nullable=False)
    dosage: Mapped[str] = mapped_column(nullable=False)
    duration: Mapped[str] = mapped_column(nullable=False)
    note: Mapped[str] = mapped_column(Text, nullable=True)

    consultation: Mapped['Consultation'] = relationship(
        back_populates="prescriptions",  uselist=False)
