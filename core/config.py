from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- App ---
    APP_NAME: str = "crypto-market-etl-pipeline"
    ENV: str = "development"

    # --- Database ---
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "crypto_etl"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "root"

    # --- External APIs ---
    CMC_API_KEY: str = ""
    CMC_BASE_URL: str = "https://pro-api.coinmarketcap.com/public-api/v3"
    BINANCE_FUTURES_BASE_URL: str = "https://fapi.binance.com"

    # --- ETL defaults ---
    CMC_TOTAL_RECORDS: int = 8089
    CMC_PAGE_SIZE: int = 5000
    HTTP_TIMEOUT_SECONDS: int = 20

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance so we don't re-parse env vars on every call."""
    return Settings()
