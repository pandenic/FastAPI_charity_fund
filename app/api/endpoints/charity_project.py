"""Contains endpoints description for charity projects processing."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_and_get_charity_project_if_exists,
    check_charity_project_fully_invested_on_update,
    check_charity_project_invested_on_delete,
    check_charity_project_name_duplication,
    check_full_amount_gte_invested_amount_on_update)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectDB,
                                         TCharityProjectCreate,
                                         TCharityProjectUpdate)
from app.services.investing import investing_after_create_charity_project

router = APIRouter()


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Return list of all charity projects."""
    return await charity_project_crud.get_multi(session)


@router.post(
    '/',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
    response_model_exclude_none=True,
)
async def create_new_charity_project(
    charity_project: TCharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new charity project."""
    await check_charity_project_name_duplication(
        charity_project_name=charity_project.name,
        session=session,
    )
    new_charity_project = await charity_project_crud.create(
        charity_project,
        session,
    )
    await investing_after_create_charity_project(new_charity_project, session)
    return new_charity_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    updated_data: TCharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update a charity project partly."""
    charity_project = await check_and_get_charity_project_if_exists(
        charity_project_id=project_id,
        session=session,
    )
    check_charity_project_fully_invested_on_update(charity_project)
    check_full_amount_gte_invested_amount_on_update(
        updated_data,
        charity_project,
    )
    if updated_data.name:
        await check_charity_project_name_duplication(
            charity_project_name=updated_data.name,
            session=session,
            charity_project_id=project_id,
        )
    charity_project = await charity_project_crud.update(
        db_obj=charity_project,
        obj_in=updated_data,
        session=session,
    )
    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a charity project if it was not invested."""
    charity_project = await check_and_get_charity_project_if_exists(
        charity_project_id=project_id,
        session=session,
    )
    check_charity_project_invested_on_delete(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project,
        session,
    )
    return charity_project
