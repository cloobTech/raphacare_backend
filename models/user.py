#!/usr/bin/python3
""" User Model for Project """
from enum import Enum as pyEnum
from datetime import datetime
from sqlalchemy import String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from utils.hash_password import hash_password
from models.base_model import BaseModel, Base


class UserType(str, pyEnum):
    """ User Type Enum """
    admin = 'admin'
    medical_practitioner = 'medical_practitioner'
    patient = 'patient'


class User(BaseModel, Base):
    """ User Class """
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(60), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(
        String(60), nullable=True)
    user_type: Mapped[str] = mapped_column(
        Enum(UserType), nullable=False)
    reset_token: Mapped[str | None] = mapped_column(
        String(60), nullable=True, default="")
    token_created_at: Mapped[datetime] = mapped_column(nullable=True)
    email_verified: Mapped[bool] = mapped_column(nullable=False, default=False)
    disabled: Mapped[bool] = mapped_column(nullable=False, default=False)
    user_profile_id: Mapped[str] = mapped_column(
        nullable=True)

    patient: Mapped['Patient'] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan")
    medical_practitioner: Mapped['MedicalPractitioner'] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan")
    admin: Mapped['Admin'] = relationship(
        back_populates="user", uselist=False, cascade="all, delete-orphan")
    notifications: Mapped[list['Notification']] = relationship(
        back_populates="user", cascade="all, delete-orphan")

    def __init__(self, *args, **kwargs):
        """
            instantiation of new User Class
        """
        if kwargs:
            if 'password' in kwargs:
                hashed_pwd = hash_password(kwargs['password'])
                kwargs['password'] = hashed_pwd
        super().__init__(*args, **kwargs)
