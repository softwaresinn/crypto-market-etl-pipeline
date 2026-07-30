import httpx
import asyncio
from datetime import datetime

cmc_url = "https://pro-api.coinmarketcap.com/public-api/v3/cryptocurrency/listings/latest"

async def getMetrics(total_needed=8000, page_size=5000):
    headers = {
        "Accept": "application/json",
    }

    all_coins = []
    start = 1  # CMC pagination is 1-indexed

    async with httpx.AsyncClient(timeout=20) as client:
        while len(all_coins) < total_needed:
            remaining = total_needed - len(all_coins)
            limit = min(page_size, remaining)

            params = {
                "start": start,
                "limit": limit,
                "convert": "USD",
            }

            res = await client.get(cmc_url, headers=headers, params=params)
            res.raise_for_status()
            data = res.json()

            batch = data.get("data", [])
            if not batch:
                # No more data returned — stop early
                break

            all_coins.extend(batch)
            start += len(batch)

            print(f"Fetched {len(batch)} coins, total so far: {len(all_coins)}")

    return all_coins