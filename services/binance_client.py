import logging
import httpx
from core.config import get_settings

logger = logging.getLogger(__name__)


async def get_futures_symbols() -> list[dict]:
    """Fetch all USDT-M futures symbols from Binance."""
    settings = get_settings()
    url = f"{settings.BINANCE_FUTURES_BASE_URL}/fapi/v1/exchangeInfo"

    async with httpx.AsyncClient(timeout=settings.HTTP_TIMEOUT_SECONDS) as client:
        res = await client.get(url)
        res.raise_for_status()
        data = res.json()

    coins = data.get("symbols", [])
    logger.info("Fetched %d futures symbols from Binance", len(coins))
    return coins
