import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPEN_AI_KEY: str = os.getenv("OPEN_AI_KEY", "")

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
