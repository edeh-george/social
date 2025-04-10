from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: str = "dev"
    DATABASE_URL: str = ""
    DB_FORCE_ROLL_BACK: bool = False

    model_config = SettingsConfigDict(
        env_file="../.env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="allow",
    )


class DevConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="DEV_")


class ProdConfig(BaseConfig):
    model_config = SettingsConfigDict(env_prefix="PROD_")


class TestConfig(BaseConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True
    model_config = SettingsConfigDict(env_prefix="TEST_")


@lru_cache()
def get_config(env_state: str) -> BaseConfig:
    config_classes = {
        "dev": DevConfig,
        "prod": ProdConfig,
        "test": TestConfig,
    }
    config_class = config_classes.get(env_state, DevConfig)
    return config_class()


# Initialize configuration based on the ENV_STATE
config = get_config(BaseConfig().ENV_STATE)
