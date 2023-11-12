"""Contain Donation model description."""
from typing import TypeVar

from sqlalchemy import Column, ForeignKey, Integer, Text

from app.core.db import Base
from app.models.base import BaseModel


class Donation(Base, BaseModel):
    """Contain Donation model description."""

    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        """Describe how object in a model will be represented."""
        return (
            f'User {self.user_id}. '
            f'Внёс {self.invested_amount}. '
            f'Комментарий: {self.comment}.'
        )


TDonation = TypeVar('TDonation', bound=Donation)
