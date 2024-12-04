#!/usr/bin/python3
""" Subscription Model for Project """
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base_model import BaseModel, Base


class Subscription(BaseModel, Base):
    """ Subscription Model """
    __tablename__ = 'subscriptions'

    patient_id: Mapped[str] = mapped_column(
        ForeignKey('patients.id'), nullable=False)
    plan_id: Mapped[str] = mapped_column(nullable=False)
    start_date: Mapped[datetime] = mapped_column(nullable=False)
    next_billing_date: Mapped[datetime] = mapped_column(
        nullable=False)
    plan_name: Mapped[str] = mapped_column(nullable=False)
    plan_price: Mapped[float] = mapped_column(nullable=False)

    patient: Mapped['Patient'] = relationship(back_populates='subscription')
