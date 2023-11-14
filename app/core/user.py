"""Describe core settings for users processing."""
from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (BaseUserManager, FastAPIUsers, IntegerIDMixin,
                           InvalidPasswordException)
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Provide async user access to DB."""
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy(token_lifetime=None) -> JWTStrategy:
    """Define secret word and lifetime for JWT."""
    return JWTStrategy(secret=settings.secret, lifetime_seconds=settings.TOKEN_LIFETIME)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Define user manger.

    Allows authentication, signing up, password reset, verification etc
    """

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """Validate password."""
        if len(password) < settings.PASSWORD_LENGTH:
            raise InvalidPasswordException(
                reason=f'Password should be at least '
                       f'{settings.PASSWORD_LENGTH} characters',
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail',
            )

    async def on_after_register(
        self,
        user: User,
        request: Optional[Request] = None,
    ):
        """Contain actions after register."""
        print(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(user_db=Depends(get_user_db)):
    """Return a user manager obj."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
