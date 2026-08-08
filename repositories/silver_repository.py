import json
from db.session import get_connection
from transformations.bronze_to_silver import *
# Insert transformations of bronze.metrics into silver.metrics.

def insert_silver_metrics() -> None:
    sql = f"""
INSERT INTO silver.metrics (
    cmc_id,
    cmc_rank,
    asset_name,
    symbol,
    infinite_supply,
    circulating_supply,
    total_supply,
    max_supply,
    self_reported_circulating_supply,
    date_added,
    last_updated,
    tvl_ratio,
    market_cap,
    fully_diluted_market_cap,
    market_cap_dominance,
    self_reported_market_cap,
    minted_market_cap,
    price,
    volume_24hr,
    cex_volume_24h,
    dex_volume_24h,
    volume_pct_change_24h,
	percent_change_24h,
    percent_change_7d,
    percent_change_30d,
    percent_change_60d,
    percent_change_90d
)

{transform_metrics}

    """

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE silver.metrics")
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()


# Insert transformation of Binance futures pairs from bronze.binance_future_pairs to silver layer

def insert_silver_binance_future() -> None:
    sql = f"""
    INSERT INTO silver.binance_future_pairs(
    symbol,
    cmc_id,
    base_asset,
    underlying_type,
    underlying_sub_type,
    onboard_date
    )   

    {transform_binance_future_pairs}
    """

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE silver.binance_future_pairs")
            cur.execute(sql)
        conn.commit()
    finally:
        conn.close()
