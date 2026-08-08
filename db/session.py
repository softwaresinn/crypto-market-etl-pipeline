import psycopg
from core.config import get_settings


def get_connection() -> psycopg.Connection:
    """Open a new Postgres connection using settings from the environment."""
    settings = get_settings()
    return psycopg.connect(
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
    )
