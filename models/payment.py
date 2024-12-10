#!/usr/bin/python3
""" Payment Model for Project """
from enum import Enum as pyEnum
from sqlalchemy import ForeignKey, Text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class PaymentStatus(str, pyEnum):
    """ Transaction Status Enum """
    pending = "pending"
    success = "success"
    failed = "failed"
    cancelled = "cancelled"


class Payment(BaseModel, Base):
    __tablename__ = "payments"

    user_id: Mapped[str] = mapped_column(
        ForeignKey('users.id'), nullable=False)
    service_id: Mapped[str] = mapped_column(
        ForeignKey('services.id'), nullable=False)
    other_service_id: Mapped[str | None] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus), nullable=False, default=PaymentStatus.pending)
    service_name: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(back_populates="payments")
    service: Mapped["Service"] = relationship(back_populates="payments")
