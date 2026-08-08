# -- Query to create binance_future_pairs,metrics on silver layer

CREATE_SILVER_TABLES= """CREATE SCHEMA IF NOT EXISTS silver;
CREATE TABLE IF NOT EXISTS silver.binance_future_pairs(
	symbol TEXT PRIMARY KEY,
	cmc_id BIGINT,
    base_asset TEXT NOT NULL,
    underlying_type TEXT,
    underlying_sub_type TEXT,
    onboard_date TIMESTAMP,
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS silver.metrics(
cmc_id BIGINT PRIMARY KEY,
cmc_rank INT,
asset_name VARCHAR,
symbol VARCHAR,
infinite_supply BOOLEAN,
circulating_supply NUMERIC, --history              
total_supply NUMERIC,                     
max_supply NUMERIC,
self_reported_circulating_supply NUMERIC,
date_added TIMESTAMPTZ,
last_updated TIMESTAMPTZ,
tvl_ratio DECIMAL,
market_cap NUMERIC, --history
fully_diluted_market_cap NUMERIC,
market_cap_dominance NUMERIC,
self_reported_market_cap NUMERIC,
minted_market_cap NUMERIC,
price NUMERIC,			--history
volume_24hr NUMERIC,     --history
cex_volume_24h NUMERIC,  --history 
dex_volume_24h NUMERIC,  --history
volume_pct_change_24h NUMERIC,
percent_change_24h NUMERIC,
percent_change_7d NUMERIC,
percent_change_30d NUMERIC,
percent_change_60d NUMERIC,
percent_change_90d NUMERIC,
inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

"""

