"""Define user pydentic schemas."""
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    """Default fastapi_users.schemas Read class."""

    pass


class UserCreate(schemas.BaseUserCreate):
    """Default fastapi_users.schemas Create class."""

    pass


class UserUpdate(schemas.BaseUserUpdate):
    """Default fastapi_users.schemas Update class."""

    pass
