import logging
import httpx
from core.config import get_settings

logger = logging.getLogger(__name__)


async def get_latest_listings(total_needed: int | None = None, page_size: int | None = None) -> list[dict]:
    """Fetch the latest cryptocurrency listings from CoinMarketCap, paginated."""
    settings = get_settings()
    total_needed = total_needed or settings.CMC_TOTAL_RECORDS
    page_size = page_size or settings.CMC_PAGE_SIZE

    url = f"{settings.CMC_BASE_URL}/cryptocurrency/listings/latest"
    headers = {
        "Accept": "application/json",
        "X-CMC_PRO_API_KEY": settings.CMC_API_KEY,
    }

    all_coins: list[dict] = []
    start = 1  # CMC pagination is 1-indexed

    async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
        while len(all_coins) < total_needed:
            remaining = total_needed - len(all_coins)
            limit = min(page_size, remaining)

            params = {"start": start, "limit": limit, "convert": "USD"}

            res = await client.get(url, headers=headers, params=params)
            res.raise_for_status()
            data = res.json()

            batch = data.get("data", [])
            if not batch:
                break  # No more data returned — stop early

            all_coins.extend(batch)
            start += len(batch)

            logger.info("Fetched %d coins, total so far: %d", len(batch), len(all_coins))

    return all_coins
