"""Data-access functions (repository layer) for curated and bronze tables."""
import json
from db.session import get_connection



def dump_cmc_json(api_response: list[dict]) -> None:
    """Land raw CoinMarketCap payloads into bronze.metrics."""
    sql = """
    INSERT INTO bronze.metrics (raw_payload)
    VALUES (%s)
    """
    data_to_insert = [(json.dumps(metrics),) for metrics in api_response]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE bronze.metrics")
            cur.executemany(sql, data_to_insert)
        conn.commit()
    finally:
        conn.close()


def dump_binance_future(api_response: list[dict]) -> None:
    """Land raw Binance futures payloads into bronze.binance_future_pairs."""
    sql = """
    INSERT INTO bronze.binance_future_pairs (raw_payload)
    VALUES (%s)
    """
    data_to_insert = [(json.dumps(future_pair),) for future_pair in api_response]

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE bronze.binance_future_pairs")
            cur.executemany(sql, data_to_insert)
        conn.commit()
    finally:
        conn.close()
