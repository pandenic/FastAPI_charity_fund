"""Contain Base abstract model description."""
from datetime import datetime
from typing import TypeVar

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer


class BaseModel:
    """Contain mandatory models' fields."""

    full_amount = Column(
        Integer,
        nullable=False,
    )
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.now)
    close_date = Column(DateTime)
    CheckConstraint('full_amount > 0', name='full_amount_gt_zero')
    CheckConstraint(
        'full_amount >= invested_amount',
        name='full_amount_ge_invested_amount',
    )


TBaseModel = TypeVar('TBaseModel', bound=BaseModel)
