#!/usr/bin/python3
""" Patient Model for Project """
from enum import Enum as pyEnum
from datetime import datetime
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class Gender(pyEnum):
    """Gender Enum Types"""
    MALE = "male"
    FEMALE = "female"
    OTHERS = "others"


class Patient(BaseModel, Base):
    """Patient class"""
    __tablename__ = "patients"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    user_name: Mapped[str] = mapped_column(String(60), nullable=False)
    emergency_contact: Mapped[str] = mapped_column(String(60), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(60), nullable=False)
    gender: Mapped[str] = mapped_column(Enum(Gender), nullable=False)
    address: Mapped[str] = mapped_column(String(60), nullable=False)
    city: Mapped[str] = mapped_column(String(60), nullable=False)
    state: Mapped[str] = mapped_column(String(60), nullable=False)
    country: Mapped[str] = mapped_column(String(60), nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(nullable=False)

    user: Mapped['User'] = relationship(
        back_populates="patient", uselist=False)
    medical_histories: Mapped[list['MedicalHistory']] = relationship(
        back_populates="patient")
