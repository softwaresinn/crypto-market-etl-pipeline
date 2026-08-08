"""
DDL definitions and table-creation helpers.

Layout follows a bronze/silver medallion convention:
  - bronze.*  raw, untransformed API payloads (landing zone)
  - public.*  cleaned/curated tables used by the API (coins, prices)
"""

from db.session import get_connection


# NOTE: previously this project created `silver.raw_metrics` here but the
# repository layer inserted into `bronze.metrics`, so raw CMC data was
# silently never landing anywhere real. Both raw tables now live
# consistently under the `bronze` schema.
CREATE_BRONZE_TABLES_SQL = """
CREATE SCHEMA IF NOT EXISTS bronze;

CREATE TABLE IF NOT EXISTS bronze.metrics (
    id SERIAL PRIMARY KEY,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_payload JSON
);

CREATE TABLE IF NOT EXISTS bronze.binance_future_pairs (
    id SERIAL PRIMARY KEY,
    inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    raw_payload JSON
);
"""



def create_raw_tables() -> None:
    """Create bronze-layer raw landing tables."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_BRONZE_TABLES_SQL)
        conn.commit()
    finally:
        conn.close()
