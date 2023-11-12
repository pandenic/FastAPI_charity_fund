"""Describe functions for investment processing."""
import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import TCharityProject, TDonation


def update_objects_when_investing(
    charity_project: TCharityProject,
    donation: TDonation,
) -> tuple[TCharityProject, TDonation]:
    """
    Update fields depend on investment data.

    If a donation or a project are fully invested or not.
    """
    money_to_invest = donation.full_amount - donation.invested_amount
    required_money = (
        charity_project.full_amount - charity_project.invested_amount
    )
    if money_to_invest >= required_money:
        donation.invested_amount += required_money
        donation.fully_invested = money_to_invest == required_money
        if donation.fully_invested:
            donation.close_date = datetime.datetime.now()
        charity_project.invested_amount = charity_project.full_amount
        charity_project.fully_invested = True
        charity_project.close_date = datetime.datetime.now()
    else:
        charity_project.invested_amount += money_to_invest
        donation.invested_amount = donation.full_amount
        donation.fully_invested = True
        donation.close_date = datetime.datetime.now()
    return charity_project, donation


async def investing_after_create_charity_project(
    charity_project: TCharityProject,
    session: AsyncSession,
):
    """
    Perform investing by updating an invested amount.

    One: CharityProject
    Many: Donation
    """
    donations = await donation_crud.get_not_fully_invested(session)

    for donation in donations:
        if charity_project.fully_invested:
            break
        charity_project, donation = update_objects_when_investing(
            charity_project,
            donation,
        )
    await charity_project_crud.add_to_commit(charity_project, session)
    await donation_crud.add_multi_to_commit(donations, session)
    await donation_crud.commit_changes(session)
    await charity_project_crud.refresh_obj(charity_project, session)
    await donation_crud.refresh_obj_multi(donations, session)


async def investing_after_making_donation(
    donation: TDonation,
    session: AsyncSession,
):
    """
    Perform investing by updating an invested amount.

    One: Donation
    Many: CharityProject
    """
    charity_projects = await charity_project_crud.get_not_fully_invested(
        session,
    )

    for charity_project in charity_projects:
        if donation.fully_invested:
            break
        charity_project, donation = update_objects_when_investing(
            charity_project,
            donation,
        )
    await charity_project_crud.add_to_commit(donation, session)
    await donation_crud.add_multi_to_commit(charity_projects, session)
    await charity_project_crud.commit_changes(session)
    await donation_crud.refresh_obj(donation, session)
    await charity_project_crud.refresh_obj_multi(charity_projects, session)
