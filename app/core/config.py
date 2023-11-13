"""Desсribe settings and configs for a FastAPI app."""
from typing import Optional

from pydantic import BaseSettings, EmailStr

TOKEN_LIFETIME = 3600
PASSWORD_LENGTH = 3


class Settings(BaseSettings):
    """
    Contain settings.

    app_title: an app name
    database_url: database parameters for salalchemy
    secret: a secret code
    token_lifetime: lifetime of a token
    first_superuser_email: a default superuser email
    first_superuser_password: a defauld superuser password
    """

    app_title: str = 'QRKot'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None

    class Config:
        """
        Configure parameters in settings.

        env_file: a path to an env file
        """

        env_file = '.env'


settings = Settings()
