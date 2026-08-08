
# Transformation of bronze.metrics for curated layer (Silver)

transform_binance_future_pairs="""SELECT
b.raw_payload ->> 'symbol' AS symbols,
cmc.cmc_id,
b.raw_payload ->> 'baseAsset' AS base_asset,
b.raw_payload ->> 'underlyingType' AS underlying_type,
b.raw_payload -> 'underlyingSubType'->>0 AS underlying_sub_type,
TO_TIMESTAMP((b.raw_payload ->> 'onboardDate')::BIGINT / 1000)::DATE AS onboard_date
FROM bronze.binance_future_pairs b
LEFT JOIN silver.metrics cmc 
    ON UPPER(b.raw_payload->>'baseAsset') = UPPER(cmc.symbol)
WHERE b.raw_payload->>'status' = 'TRADING' AND b.raw_payload->>'quoteAsset'='USDT'
"""


transform_metrics="""SELECT DISTINCT ON (raw_payload->>'symbol')

    (raw_payload->>'id')::BIGINT,
    (raw_payload->>'cmc_rank')::INT,
    raw_payload->>'name',
    raw_payload->>'symbol',
    (raw_payload->>'infinite_supply')::BOOLEAN,
    (raw_payload->>'circulating_supply')::NUMERIC,
    (raw_payload->>'total_supply')::NUMERIC,
    (raw_payload->>'max_supply')::NUMERIC,
    (raw_payload->>'self_reported_circulating_supply')::NUMERIC,
    (raw_payload->>'date_added')::TIMESTAMPTZ,
    (raw_payload->>'last_updated')::TIMESTAMPTZ,
    (raw_payload->>'tvl_ratio')::NUMERIC,

    (raw_payload->'quote'->0->>'market_cap')::NUMERIC,
    (raw_payload->'quote'->0->>'fully_diluted_market_cap')::NUMERIC,
    (raw_payload->'quote'->0->>'market_cap_dominance')::NUMERIC,

    (raw_payload->>'self_reported_market_cap')::NUMERIC,
    (raw_payload->>'minted_market_cap')::NUMERIC,

    (raw_payload->'quote'->0->>'price')::NUMERIC,
    (raw_payload->'quote'->0->>'volume_24h')::NUMERIC,
    (raw_payload->'quote'->0->>'cex_volume_24h')::NUMERIC,
    (raw_payload->'quote'->0->>'dex_volume_24h')::NUMERIC,
    (raw_payload->'quote'->0->>'volume_change_24h')::NUMERIC,	    
	(raw_payload->'quote'->0->>'percent_change_24h')::NUMERIC,
    (raw_payload->'quote'->0->>'percent_change_7d')::NUMERIC,
    (raw_payload->'quote'->0->>'percent_change_30d')::NUMERIC,
    (raw_payload->'quote'->0->>'percent_change_60d')::NUMERIC,
    (raw_payload->'quote'->0->>'percent_change_90d')::NUMERIC

FROM bronze.metrics
ORDER BY
    raw_payload->>'symbol',
    (raw_payload->'quote'->0->>'market_cap')::NUMERIC DESC;


"""


