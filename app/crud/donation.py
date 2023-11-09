from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models import Donation
from app.schemas.donation import DonationCreate


class CRUDDonation(CRUDBase[
    Donation,
    DonationCreate,
]):

    async def get_all_for_user(
            self,
            user_id: int,
            session: AsyncSession,
    ) -> List[ModelType]:
        db_objs = await session.execute(
            select(self.model).where(
                Donation.user_id == user_id,
            )
        )
        return db_objs.scalars().all()


donation_crud = CRUDDonation(Donation)
