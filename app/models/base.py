from datetime import datetime

from sqlalchemy import Column, Integer, CheckConstraint, Boolean, DateTime, func, and_, text

from app.core.db import Base


class BaseModel:

    full_amount = Column(
        Integer,
        nullable=False,
    )
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(DateTime, default=datetime.utcnow)
    close_date = Column(DateTime)
    CheckConstraint('full_amount > 0', name='full_amount_gt_zero')
    CheckConstraint(
        'full_amount >= invested_amount',
        name='full_amount_ge_invested_amount',
    )
