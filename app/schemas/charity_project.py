"""Define charity project pydentic schemas."""
from datetime import datetime
from typing import Optional, TypeVar

from pydantic import BaseModel, Extra, Field


class CharityProjectBase(BaseModel):
    """Define mandatory fields."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        """Schema config."""

        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    """
    Define fields.

    For respresentation generally.
    """

    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        """Schema config."""

        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    """
    Define fields.

    Required to create a donation.
    """

    pass


class CharityProjectUpdate(CharityProjectBase):
    """
    Define fields.

    Required to update a donation.
    """

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)


TCharityProjectBase = TypeVar('TCharityProjectBase', bound=CharityProjectBase)
TCharityProjectDB = TypeVar('TCharityProjectDB', bound=CharityProjectDB)
TCharityProjectCreate = TypeVar(
    'TCharityProjectCreate',
    bound=CharityProjectCreate,
)
TCharityProjectUpdate = TypeVar(
    'TCharityProjectUpdate',
    bound=CharityProjectUpdate,
)
