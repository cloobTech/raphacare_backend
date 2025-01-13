from enum import Enum as PyEnum
from sqlalchemy import String, ForeignKey, JSON, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from models.base_model import BaseModel, Base


class PractitionerType(str, PyEnum):
    """Practitioner Type Enum"""
    DOCTOR = "doctor"
    NURSE = "nurse"
    COMMUNITY_HEALTH = "community_health"


class MedicalPractitioner(BaseModel, Base):
    """Medical Practitioner Class"""
    __tablename__ = "medical_practitioners"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    other_names: Mapped[str] = mapped_column(String(60), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(60), nullable=True)
    practitioner_type: Mapped[str] = mapped_column(
        Enum(PractitionerType), nullable=False)
    specialization: Mapped[str] = mapped_column(String(60), nullable=True)
    license_number: Mapped[str] = mapped_column(String(60), nullable=True)
    is_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    availability: Mapped[dict] = mapped_column(JSON, nullable=True)
    is_available: Mapped[bool] = mapped_column(nullable=False, default=True)
    profile_picture_url: Mapped[str] = mapped_column(nullable=True)
    consultation_fee: Mapped[dict] = mapped_column(JSON, nullable=True)

    user: Mapped['User'] = relationship(
        back_populates="medical_practitioner", lazy="selectin", uselist=False)
    medical_histories: Mapped[list['MedicalHistory']] = relationship(
        back_populates="medical_practitioner")
    appointments: Mapped[list['Appointment']] = relationship(
        lazy="selectin", cascade="all, delete-orphan",
        back_populates="medical_practitioner")
    services: Mapped[list['Service']] = relationship(
        lazy="selectin", back_populates="medical_practitioner", cascade="all, delete-orphan")
    health_centers: Mapped[list['HealthCenter']] = relationship(
        back_populates="medical_practitioner", lazy="selectin", cascade="all, delete-orphan")

    @validates("consultation_fee")
    def validate_consultation_fee(self, key, value):
        """
        Ensure consultation_fee contains only the allowed keys and their values are valid.
        """
        allowed_keys = {"physical", "online", "home_service"}
        if not isinstance(value, dict):
            raise ValueError("consultation_fee must be a dictionary.")
        if not allowed_keys.issuperset(value.keys()):
            raise ValueError(
                f"Invalid keys in consultation_fee. Allowed keys are: {
                    allowed_keys}."
            )
        for key in value:
            if not isinstance(value[key], (int, float)) or value[key] < 0:
                raise ValueError(
                    f"Consultation fee for {
                        key} must be a non-negative number."
                )
        return value
