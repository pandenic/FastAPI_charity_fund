"""
Contains a database preset.

class Prebase: describe mandatory fields
AsyncSessionLocal: an async session maker
get_async_session: a function to create an async session
"""
from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, declared_attr, sessionmaker

from app.core.config import settings


class PreBase:
    """
    Declare attributes for each table in DB.

    __tablename__ == model class name
    id: unique id field
    """

    @declared_attr
    def __tablename__(cls):
        """Bind table name to the class name."""
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)


Base = declarative_base(cls=PreBase)

engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Create and return async session."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
