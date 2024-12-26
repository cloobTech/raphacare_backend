from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class HealthCenter(BaseModel, Base):
    """Medical Practitioner Health Center Address"""
    __tablename__ = "health_centers"

    medical_practitioner_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("medical_practitioners.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    postal_code: Mapped[str] = mapped_column(String(20), nullable=True)

    medical_practitioner: Mapped['MedicalPractitioner'] = relationship(
        back_populates="health_centers")
