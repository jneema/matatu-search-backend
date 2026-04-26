from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from pydantic import Field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    database_url: str = Field(default=..., alias="DATABASE_URL")
    alembic_db_url: str = Field(default=..., alias="ALEMBIC_DB_URL")
    redis_url: str = Field(default=..., alias="REDIS_URL")
    secret_key: str = Field(default=..., alias="SECRET_KEY")
    algorithm: str = Field(default=..., alias="ALGORITHM")
    access_token_expire_minutes: int = Field(
        default=..., alias="ACCESS_TOKEN_EXPIRE_IN_MINUTES")
    environment: str = Field(default=..., alias="ENVIRONMENT")
    log_level: str = Field(default=..., alias="LOG_LEVEL")
    cors_origins: str = Field(default=..., alias="CORS_ORIGINS")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]

    @property
    def is_development(self) -> bool:
        return self.environment == "development"


@lru_cache
def get_settings() -> Settings:
    return Settings()
