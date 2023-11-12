"""Contain User model description."""
from typing import TypeVar

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Contain User model description."""

    pass


TUser = TypeVar('TUser', bound=User)
