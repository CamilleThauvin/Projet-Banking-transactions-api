"""Configuration module for the Banking Transactions API."""

import os
from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # CSV data path
    csv_path: str = "data/cards_data.csv"

    # Application environment
    app_env: Literal["dev", "prod"] = "dev"

    # API metadata
    api_title: str = "Banking Transactions API"
    api_version: str = "1.0.0"
    api_description: str = "API FastAPI pour exposer des transactions bancaires fictives"

    class Config:
        """Pydantic config."""

        env_file = ".env"
        case_sensitive = False


settings = Settings()

