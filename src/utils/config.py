"""Application settings loaded from environment variables."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for pk-pr-simulator."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = "postgresql+psycopg2://pkpr:devpassword@localhost:5432/pk_pr_simulator"
    wandb_project: str = "pk-pr-simulator"
    wandb_entity: str | None = None
    pkpr_random_seed: int = 42
    pkpr_data_dir: str = "./data"


@lru_cache
def get_settings() -> Settings:
    return Settings()
