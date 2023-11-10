# app/models/charity_project.py

from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.base import BaseModel


class CharityProject(Base, BaseModel):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'Благотворительный проект {self.name}. Описание: {self.description}'
        )
