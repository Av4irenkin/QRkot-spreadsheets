import os
from typing import Optional

from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.constants import APP_TITTLE, DESCRIPTION


class Settings(BaseSettings):
    app_title: str = APP_TITTLE
    model_config = SettingsConfigDict(env_file='.env')
    description: str = DESCRIPTION
    database_url: str = os.getenv(
        'DATABASE_URL',
        default='sqlite+aiosqlite:///./cat_charity.db'
    )
    secret: str = 'secret'
    first_superuser_email: Optional[EmailStr] = None
    first_superuser_password: Optional[str] = None
    email: Optional[str] = None
    type: Optional[str] = None
    project_id: Optional[str] = None
    private_key_id: Optional[str] = None
    private_key: Optional[str] = None
    client_email: Optional[str] = None
    client_id: Optional[str] = None
    auth_uri: Optional[str] = None
    token_uri: Optional[str] = None
    auth_provider_x509_cert_url: Optional[str] = None
    client_x509_cert_url: Optional[str] = None
    spreadsheet_id: Optional[str] = None


settings = Settings()
