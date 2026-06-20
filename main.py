from fastapi import FastAPI
from services.binance import get_coins

app = FastAPI()

@app.get("/symbols/usdt")
async def symbols():
    return await get_coins()