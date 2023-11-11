from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import ErrorMessage
from app.crud.charity_project import charity_project_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_name_duplication(
        charity_project_name: str,
        session: AsyncSession,
        charity_project_id: int = None,
) -> None:
    charity_project = await (
        charity_project_crud.get_charity_project_by_name(
            charity_project_name, session
        )
    )
    if charity_project and not charity_project.id == charity_project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_NAME_EXISTS,
        )


async def check_and_get_charity_project_if_exists(
        charity_project_id: int,
        session: AsyncSession,
) -> CharityProject:
    charity_project = await (
        charity_project_crud.get(
            charity_project_id, session,
        )
    )
    if not charity_project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=ErrorMessage.CHARITY_PROJECT_ID_NOT_FOUND,
        )
    return charity_project


def check_full_amount_gte_invested_amount_on_update(
        updated_data: CharityProjectUpdate,
        charity_project: CharityProject,
) -> None:
    if updated_data.full_amount and updated_data.full_amount < charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_FULL_AMOUNT_LT_INVESTED,
        )


def check_charity_project_fully_invested_on_update(
    charity_project: CharityProject,
) -> None:
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_FULLY_INVESTED,
        )


def check_charity_project_invested_on_delete(
    charity_project: CharityProject,
) -> None:
    if charity_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail=ErrorMessage.CHARITY_PROJECT_PARTLY_INVESTED,
        )