from datetime import datetime

from pydantic import BaseModel, Field, Extra


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: str = Field(None, min_length=1)

    class Config:
        extra = Extra.forbid


class DonationUserDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationUserDB):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: datetime = None

    class Config:
        orm_mode = True


class DonationCreate(DonationBase):
    pass


