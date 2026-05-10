from pydantic_settings import BaseSettings
import os
from typing import Optional

class AppConfig(BaseSettings):
    APP_NAME: str = os.getenv("APP_NAME", "Async-Task-Queue")
    APP_ENV: str = os.getenv("APP_ENV", "local")
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", 8000))
    APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "NA")
    APP_VERSION: str = os.getenv("APP_VERSION", "0.0.0")

    REDIS_HOST: Optional[str] = os.getenv("REDIS_HOST", "192.168.5.192")
    REDIS_PORT: Optional[int] = int(os.getenv("REDIS_PORT", 6379))
    REDIS_DB: Optional[int] = int(os.getenv("REDIS_DB", 0))
    REDIS_AUTH_TOKEN: Optional[str] = os.getenv("REDIS_AUTH_TOKEN") or None
    REDIS_SSL: bool = os.getenv("REDIS_SSL", "false").lower() == "true"

    class Config:
        case_sensitive = True
        env_file = ".env"

appconfig = AppConfig()