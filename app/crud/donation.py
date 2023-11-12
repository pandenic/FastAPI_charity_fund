"""Describe Donation CRUD model operations."""
from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models import Donation, TDonation
from app.schemas.donation import TDonationCreate


class CRUDDonation(
    CRUDBase[
        TDonation,
        TDonationCreate,
        None,
    ],
):
    """
    Describe Donation CRUD.

    get_all_for_user: return a list of objs for by user
    """

    async def get_all_for_user(
        self,
        user_id: int,
        session: AsyncSession,
    ) -> List[ModelType]:
        """Return a list of objs for by user."""
        db_objs = await session.execute(
            select(self.model).where(
                Donation.user_id == user_id,
            ),
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
