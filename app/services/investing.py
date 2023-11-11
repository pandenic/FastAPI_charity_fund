import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import CharityProject, Donation


def update_objects_when_investing(
        charity_project: CharityProject,
        donation: Donation,
) -> tuple[CharityProject, Donation]:
    money_to_invest = donation.full_amount - donation.invested_amount
    required_money = charity_project.full_amount - charity_project.invested_amount
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
        charity_project: CharityProject,
        session: AsyncSession,
):
    donations = await (
        donation_crud.get_not_fully_invested(session)
    )

    for donation in donations:
        if charity_project.fully_invested:
            break
        charity_project, donation = update_objects_when_investing(
            charity_project, donation,
        )
    await charity_project_crud.update_when_investing(charity_project, session)
    await donation_crud.update_multi_when_investing(donations, session)
    await session.commit()
    await session.refresh(charity_project)
    for donation in donations:
        await session.refresh(donation)


async def investing_after_making_donation(
        donation: Donation,
        session: AsyncSession,
):
    charity_projects = await (
        charity_project_crud.get_not_fully_invested(session)
    )

    for charity_project in charity_projects:
        if donation.fully_invested:
            break
        charity_project, donation = update_objects_when_investing(
            charity_project, donation,
        )
    await donation_crud.update_when_investing(donation, session)
    await charity_project_crud.update_multi_when_investing(charity_projects, session)
    await session.commit()
    await session.refresh(donation)
    for project in charity_projects:
        await session.refresh(project)
