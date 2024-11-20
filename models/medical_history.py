#!/usr/bin/python3
""" Medical Record Model for Project """
from datetime import datetime
from sqlalchemy import String, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class MedicalHistory(BaseModel, Base):
    """Medical History Class"""
    __tablename__ = "medical_histories"

    patient_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("patients.id"), nullable=False)
    medical_practioner_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("medical_practitioners.id"), nullable=True)
    type: Mapped[str] = mapped_column(String(60), nullable=False)
    description: Mapped[str] = mapped_column(String(60), nullable=False)
    notes: Mapped[str] = mapped_column(Text, nullable=False)
    date: Mapped[datetime] = mapped_column(nullable=False)

    patient: Mapped['Patient'] = relationship(
        back_populates="medical_histories", uselist=False)
    medical_practitioner: Mapped['MedicalPractitioner'] = relationship(
        back_populates="medical_histories", uselist=False)
