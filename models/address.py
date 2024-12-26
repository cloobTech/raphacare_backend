from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class Address(BaseModel, Base):
    """Address Model for Home Service"""
    __tablename__ = "addresses"

    appointment_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("appointments.id"), nullable=False)
    street: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)

    appointment: Mapped['Appointment'] = relationship(
        back_populates="address", uselist=False)
