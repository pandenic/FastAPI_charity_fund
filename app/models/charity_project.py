"""Contain CharityProject model description."""
from typing import TypeVar

from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.base import BaseModel


class CharityProject(Base, BaseModel):
    """Contain CharityProject model description."""

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        """Describe how object in a model will be represented."""
        return (
            f'Благотворительный проект {self.name}. '
            f'Описание: {self.description}'
        )


TCharityProject = TypeVar('TCharityProject', bound=CharityProject)
