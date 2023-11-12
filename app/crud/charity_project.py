"""Describe CharityProject CRUD model operations."""
from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models import CharityProject
from app.models.charity_project import TCharityProject
from app.schemas.charity_project import (TCharityProjectCreate,
                                         TCharityProjectUpdate)


class CRUDCharityProject(
    CRUDBase[
        TCharityProject,
        TCharityProjectCreate,
        TCharityProjectUpdate,
    ],
):
    """
    Describe CharityProject CRUD.

    get: return an obj by id
    update: update an obj with new data depend on if project invested or not
    remove: delete an object
    get_charity_project_by_name: return an obj by name
    """

    async def get(
        self,
        obj_id: int,
        session: AsyncSession,
    ) -> Optional[ModelType]:
        """Return an obj by id."""
        db_obj = await session.execute(
            select(self.model).where(self.model.id == obj_id),
        )
        return db_obj.scalars().first()

    async def update(
        self,
        db_obj: TCharityProject,
        obj_in: TCharityProjectUpdate,
        session: AsyncSession,
    ) -> ModelType:
        """Update an obj with new data depend on if project invested or not."""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        if db_obj.full_amount == db_obj.invested_amount:
            db_obj.fully_invested = True
            db_obj.close_date = datetime.now()
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self,
        db_obj: TCharityProject,
        session: AsyncSession,
    ) -> ModelType:
        """Delete an object."""
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_charity_project_by_name(
        self,
        charity_project_name: str,
        session: AsyncSession,
    ) -> CharityProject:
        """Return an obj by name."""
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project_name,
            ),
        )
        return project.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
