import psycopg

def get_connection():
    conn = psycopg.connect(
        host="localhost",
        port=5432,
        dbname="crypto_etl",
        user="postgres",
        password="root"
    )
    return conn


CREATE_TABLES_SQL = """
CREATE TABLE IF NOT EXISTS coins (
    symbol TEXT PRIMARY KEY,
    base_asset TEXT NOT NULL,
    underlying_type TEXT,
    underlying_sub_type TEXT[],
    onboard_date TIMESTAMP,
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS prices (
    id BIGSERIAL PRIMARY KEY,
    symbol TEXT NOT NULL REFERENCES coins(symbol),
    price NUMERIC NOT NULL,
    ts TIMESTAMP NOT NULL,
    UNIQUE(symbol, ts)
);

CREATE INDEX IF NOT EXISTS idx_prices_symbol_ts ON prices(symbol, ts DESC);
"""


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLES_SQL)
        conn.commit()
    finally:
        conn.close()


def upsert_coins(coins: list[dict]):
    sql = """
    INSERT INTO coins (symbol, base_asset, underlying_type, underlying_sub_type, onboard_date, updated_at)
    VALUES (%(symbol)s, %(base_asset)s, %(underlying_type)s, %(underlying_sub_type)s, %(onboardDate)s, now())
    ON CONFLICT (symbol) DO UPDATE SET
        base_asset = EXCLUDED.base_asset,
        underlying_type = EXCLUDED.underlying_type,
        underlying_sub_type = EXCLUDED.underlying_sub_type,
        onboard_date = EXCLUDED.onboard_date,
        updated_at = now();
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.executemany(sql, coins)
        conn.commit()
    finally:
        conn.close()


def insert_prices(merged: list[dict]):
    """merged rows must contain symbol, price, and time keys"""

    sql = """
    INSERT INTO prices (symbol, price, ts)
    VALUES (%(symbol)s, %(price)s, %(time)s)
    ON CONFLICT (symbol, ts) DO NOTHING;
    """
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE prices;")
            cur.executemany(sql, merged)
        conn.commit()
    finally:
        conn.close()