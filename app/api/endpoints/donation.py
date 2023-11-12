"""
Contain donation endpoints description.

get_all_donations: return all donations; superuser only
create_donation: create and return donaion; active user only
get_all_donations_for_user: return all donations for a user
"""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import TUser
from app.schemas.donation import DonationDB, DonationUserDB, TDonationCreate
from app.services.investing import investing_after_making_donation

router = APIRouter()


@router.get(
    '/',
    response_model=list[DonationDB],
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
):
    """Return all donations."""
    return await donation_crud.get_multi(session)


@router.post(
    '/',
    response_model=DonationUserDB,
    dependencies=[Depends(current_user)],
    response_model_exclude_none=True,
)
async def create_donation(
    donation: TDonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: TUser = Depends(current_user),
):
    """Create a new donation."""
    new_donation = await donation_crud.create(donation, session, user)
    await investing_after_making_donation(new_donation, session)
    return new_donation


@router.get(
    '/my',
    response_model=list[DonationUserDB],
    dependencies=[Depends(current_user)],
)
async def get_all_donations_for_user(
    user: TUser = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Return all user's donations."""
    return await donation_crud.get_all_for_user(user.id, session)
