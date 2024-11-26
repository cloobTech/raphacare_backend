#!/usr/bin/python3
""" Patient Model for Project """
from enum import Enum as pyEnum
from datetime import datetime
from sqlalchemy import String, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class Gender(str, pyEnum):
    """Gender Enum Types"""
    male = "male"
    female = "female"
    others = "others"


class Patient(BaseModel, Base):
    """Patient class"""
    __tablename__ = "patients"

    user_id: Mapped[str] = mapped_column(
        String(60), ForeignKey("users.id"), nullable=False)
    first_name: Mapped[str] = mapped_column(String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(String(60), nullable=False)
    other_names: Mapped[str] = mapped_column(String(60), nullable=True)
    user_name: Mapped[str] = mapped_column(String(60), nullable=True)
    emergency_contact: Mapped[str] = mapped_column(String(60), nullable=True)
    phone_number: Mapped[str] = mapped_column(String(60), nullable=True)
    gender: Mapped[str] = mapped_column(Enum(Gender), nullable=True)
    address: Mapped[str] = mapped_column(String(60), nullable=True)
    city: Mapped[str] = mapped_column(String(60), nullable=True)
    state: Mapped[str] = mapped_column(String(60), nullable=True)
    country: Mapped[str] = mapped_column(String(60), nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(nullable=True)

    user: Mapped['User'] = relationship(
        back_populates="patient", lazy="selectin", uselist=True)
    medical_histories: Mapped[list['MedicalHistory']] = relationship(
        back_populates="patient")
    appointments: Mapped[list['Appointment']] = relationship(
       lazy="selectin", back_populates="patient")
