from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    database_url: str = "sqlite:///./app.db"

    secret_key: str = "dev-secret-change-in-production__"
    db_force_rollback: bool = False

    debug: bool = False
    allowed_hosts: str = Field(default="localhost")

    model_config = SettingsConfigDict(case_sensitive=False, env_file_encoding="utf-8")

    @field_validator("secret_key")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("Secret key must be at least 32 characters")
        return v


@lru_cache()
def get_environment() -> str:
    import os

    from dotenv import load_dotenv

    load_dotenv()
    return os.getenv("ENVIRONMENT", "development").lower()


@lru_cache()
def get_config(env_state: Optional[str] = None) -> Settings:
    env_state = env_state or get_environment()

    env_files = {
        "production": BASE_DIR / ".env.prod",
        "testing": BASE_DIR / ".env.test",
        "development": BASE_DIR / ".env.dev",
    }

    env_file = env_files.get(env_state, BASE_DIR / ".env.dev")

    try:
        return Settings(_env_file=str(env_file) if env_file.exists() else None)
    except Exception as e:
        print(f"Configuration error: {e}")
        return Settings()


config = get_config()


if __name__ == "__main__":
    # print(BASE_DIR)
    pass
