from fastapi import FastAPI
from fastapi.concurrency import run_in_threadpool
from services.binance import getCoins, getCurrentPrice, cleanData
from services.cmc import getMetrics
from models.db import init_db, upsert_coins, insert_prices

app = FastAPI()

@app.get("/symbols")
async def symbols():
    return await getCoins()


@app.get("/currentprice")
async def currentprice():
    return await getCurrentPrice()

@app.get("/cleandata")
async def cleandata():
    coins, merged = await cleanData()
    return merged

@app.get("/metrics")
async def getmetrics():
    metrics = await getMetrics()
    return metrics

@app.post("/etl/run")
async def run_etl():
    coins, merged = await cleanData()
    await run_in_threadpool(upsert_coins, coins)
    await run_in_threadpool(insert_prices, merged)
    return {"coins_upserted": len(coins), "prices_inserted": len(merged)}