# app/models/donation.py
from typing import TypeVar

from sqlalchemy import Column, Text, Integer, ForeignKey

from app.core.db import Base
from app.models.base import BaseModel


class Donation(Base, BaseModel):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (
            f'User {self.user_id}. '
            f'Внёс {self.invested_amount}. '
            f'Комментарий: {self.comment}.'
        )
