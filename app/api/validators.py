"""Contain validators for the project."""
from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ErrorMessage
from app.crud.charity_project import charity_project_crud
from app.models import TCharityProject
from app.schemas.charity_project import TCharityProjectUpdate


async def check_charity_project_name_duplication(
    charity_project_name: str,
    session: AsyncSession,
    charity_project_id: int = None,
) -> None:
    """Check if an entered charity project name duplicates an existed name."""
    charity_project = await charity_project_crud.get_charity_project_by_name(
        charity_project_name,
        session,
    )
    if charity_project and charity_project.id != charity_project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_NAME_EXISTS,
        )


async def check_and_get_charity_project_if_exists(
    charity_project_id: int,
    session: AsyncSession,
) -> TCharityProject:
    """Check if a charity project exists and get the object."""
    charity_project = await charity_project_crud.get(
        charity_project_id,
        session,
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessage.CHARITY_PROJECT_ID_NOT_FOUND,
        )
    return charity_project


def check_full_amount_gte_invested_amount_on_update(
    updated_data: TCharityProjectUpdate,
    charity_project: TCharityProject,
) -> None:
    """
    Check if an amount to be invested >= invested amount.

    If in a charity project amount of money to be invested
    greater than or equal invested amount.
    """
    if (
        updated_data.full_amount and
        updated_data.full_amount < charity_project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_FULL_AMOUNT_LT_INVESTED,
        )


def check_charity_project_fully_invested_on_update(
    charity_project: TCharityProject,
) -> None:
    """Check if a charity project is fully invested."""
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_FULLY_INVESTED,
        )


def check_charity_project_invested_on_delete(
    charity_project: TCharityProject,
) -> None:
    """Check if a charity project is partly invested before deleting."""
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_PARTLY_INVESTED,
        )
