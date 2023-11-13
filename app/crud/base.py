"""Describe base CRUD operations."""
from typing import Generic, List, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base
from app.models import User

ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
    ],
):
    """
    Describe base CRUD.

    get_multi: return all obj
    create: create an obj
    get_not_fully_invested: return not fully invested obj
    update_when_investing: update an object on investing process
    update_multi_when_investing: update a list of objects on investing
    """

    def __init__(self, model: Type[ModelType]):
        """Initialize model."""
        self.model = model

    async def commit_changes(
        self,
        session: AsyncSession,
    ):
        """Commit model changes."""
        await session.commit()

    async def refresh_obj(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ):
        """Refresh an objects."""
        await session.refresh(db_obj)

    async def refresh_obj_multi(
        self,
        db_objs: list[ModelType],
        session: AsyncSession,
    ):
        """Refresh a list of objects."""
        for db_obj in db_objs:
            await session.refresh(db_obj)

    async def get_multi(self, session: AsyncSession) -> List[ModelType]:
        """Return all objects."""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        user: Optional[User] = None,
    ) -> ModelType:
        """Create an obj."""
        obj_in_data = obj_in.dict()
        if user:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await self.commit_changes(session)
        await self.refresh_obj(db_obj, session)
        return db_obj

    async def get_not_fully_invested(
        self,
        session: AsyncSession,
    ) -> List[ModelType]:
        """Return a not fully invested obj."""
        db_objs = await session.execute(
            select(self.model).where(
                self.model.fully_invested == 0,
            ),
        )
        return db_objs.scalars().all()

    async def add_to_commit(
        self,
        db_obj: ModelType,
        session: AsyncSession,
    ) -> None:
        """Update an obj on investing."""
        session.add(db_obj)

    async def add_multi_to_commit(
        self,
        db_objs: list[ModelType],
        session: AsyncSession,
    ) -> None:
        """Update a list of obj on investing."""
        for db_obj in db_objs:
            session.add(db_obj)
