from datetime import datetime
from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase, ModelType
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectCreate


class CRUDCharityProject(CRUDBase[
    CharityProject,
    CharityProjectCreate,
]):

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession,
    ) -> ModelType:
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
            db_obj,
            session: AsyncSession,
    ) -> ModelType:
        await session.delete(db_obj)
        await session.commit()
        return db_obj

    async def get_charity_project_by_name(
            self,
            charity_project_name: str,
            session: AsyncSession
    ) -> CharityProject:
        project = await session.execute(
            select(CharityProject).where(
                CharityProject.name == charity_project_name,
            )
        )
        return project.scalars().first()


charity_project_crud = CRUDCharityProject(CharityProject)
