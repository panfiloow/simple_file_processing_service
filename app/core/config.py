from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    # Основные настройки
    VERSION : str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # Настройки базы данных
    DATABASE_URL: Optional[str] = None

    # JWT настройки
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

settings = Settings()