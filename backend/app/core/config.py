"""Application configuration using Pydantic Settings.

Loads environment variables from .env file with type validation.
"""
from functools import lru_cache
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Database
    DATABASE_URL: str = Field(
        default="postgresql://inventory_user:inventory_password@localhost:5432/inventory_db",
        description="PostgreSQL database connection URL",
    )
    POSTGRES_USER: str = "inventory_user"
    POSTGRES_PASSWORD: str = "inventory_password"
    POSTGRES_DB: str = "inventory_db"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    # Application
    PROJECT_NAME: str = "Inventory & Order Management System"
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False
    SECRET_KEY: str = "change-me"
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://localhost:5173"

    @field_validator("ALLOWED_ORIGINS")
    @classmethod
    def parse_allowed_origins(cls, v: str) -> List[str]:
        """Parse comma-separated origins into a list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    @property
    def allowed_origins_list(self) -> List[str]:
        """Get allowed CORS origins as a list."""
        return self.parse_allowed_origins(self.ALLOWED_ORIGINS)


@lru_cache()
def get_settings() -> Settings:
    """Cached settings instance for dependency injection."""
    return Settings()


settings = get_settings()
