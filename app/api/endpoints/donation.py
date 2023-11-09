from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationDB, DonationCreate, DonationUserDB
from app.services.investing import investing_after_making_donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
        session: AsyncSession = Depends(get_async_session),
):
    all_donations = await donation_crud.get_multi(session)
    return all_donations


@router.post(
    '/',
    response_model=DonationDB,
    dependencies=[Depends(current_user)],
)
async def create_donation(
        donation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    new_donation = await donation_crud.create(donation, session, user)
    await investing_after_making_donation(new_donation, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    dependencies=[Depends(current_user)],
)
async def get_all_donations_for_user(
        user: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    donations = await donation_crud.get_all_for_user(user.id, session)
    return donations
