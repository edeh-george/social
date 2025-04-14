from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

BASE_DIR = Path(__file__).resolve().parent
ENV_FILE = BASE_DIR / ".env"


class BaseConfig(BaseSettings):
    ENV_STATE: Optional[str] = Field(default="", env="ENV_STATE")
    DATABASE_URL: Optional[str] = Field(default="", env="DATABASE_URL")
    DB_FORCE_ROLL_BACK: bool = False
    SECRET_KEY: str = Field(default="", env="SECRET_KEY")

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


class DevConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="DEV_",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


class ProdConfig(BaseConfig):
    model_config = SettingsConfigDict(
        env_prefix="PROD_",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


class TestConfig(BaseConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True
    SECRET_KEY: str = "test-secret"

    model_config = SettingsConfigDict(
        env_prefix="TEST_",
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )



@lru_cache()
def get_config(env_state: Optional[str] = None) -> BaseConfig:
    env_state = env_state or BaseConfig().ENV_STATE
    config_classes = {
        "dev": DevConfig,
        "prod": ProdConfig,
        "test": TestConfig,
    }
    config_class = config_classes.get(env_state.lower(), DevConfig)
    return config_class()

config = get_config(BaseConfig().ENV_STATE)
