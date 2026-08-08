import logging
from fastapi import APIRouter, HTTPException
from core.config import get_settings
from repositories.bronze_repository import dump_binance_future
from services.binance_client import get_futures_symbols

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/etl", tags=["etl"])



@router.post("/binance-future-pairs/ingest")
async def ingest_binance_future_pairs():
    try:
        records = await get_futures_symbols()
        total_ingested = len(records)

        if total_ingested == 0:
            raise HTTPException(status_code=500, detail="No data received from Binance Futures API.")

        dump_binance_future(records)

        return {
            "status": "success",
            "pipeline_type": "Bronze Ingestion Only",
            "records_dumped_to_bronze.binance_future_pairs": total_ingested,
            "message": "Binance Future Pairs successfully archived. Curated coins/prices tables were not affected.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Binance future pairs ingestion failed")
        raise HTTPException(status_code=500, detail=f"Binance Future Pairs Ingestion Failed: {str(e)}")




