"""Define donation pydentic schemas."""
from datetime import datetime
from typing import TypeVar

from pydantic import BaseModel, Extra, Field


class DonationBase(BaseModel):
    """Define mandatory fields."""

    full_amount: int = Field(..., gt=0)
    comment: str = Field(None, min_length=1)

    class Config:
        """Schema config."""

        extra = Extra.forbid


class DonationUserDB(DonationBase):
    """
    Define fields.

    For respresentation to user.
    """

    id: int
    create_date: datetime

    class Config:
        """Schema config."""

        orm_mode = True


class DonationDB(DonationUserDB):
    """
    Define fields.

    For respresentation generally.
    """

    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime = None

    class Config:
        """Schema config."""

        orm_mode = True


class DonationCreate(DonationBase):
    """
    Define fields.

    Required to create a donation.
    """

    pass


TDonationBase = TypeVar('TDonationBase', bound=DonationBase)
TDonationUserDB = TypeVar('TDonationUserDB', bound=DonationUserDB)
TDonationDB = TypeVar('TDonationDB', bound=DonationDB)
TDonationCreate = TypeVar('TDonationCreate', bound=DonationCreate)
