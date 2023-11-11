from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra, root_validator
from app.core.errors import ErrorMessage


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime = None

    class Config:
        orm_mode = True


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int] = Field(None, gt=0)
