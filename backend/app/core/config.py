from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MODEL_PATH: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
