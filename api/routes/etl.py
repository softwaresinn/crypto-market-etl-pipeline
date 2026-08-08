import logging
from fastapi import APIRouter, HTTPException
from core.config import get_settings
from db.repository import dump_binance_future, dump_cmc_json
from services.binance_client import get_futures_symbols
from services.cmc_client import get_latest_listings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/etl", tags=["etl"])


@router.post("/cmc-metrics/ingest")
async def ingest_cmc_metrics():
    settings = get_settings()
    try:
        # 1. Asynchronously fetch records in paginated batches and land them in bronze.metrics
        records = await get_latest_listings(
            total_needed=settings.CMC_TOTAL_RECORDS,
            page_size=settings.CMC_PAGE_SIZE,
        )
        total_ingested = len(records)

        if total_ingested == 0:
            raise HTTPException(status_code=500, detail="No metrics received from CMC API.")

        dump_cmc_json(records)

        return {
            "status": "success",
            "pipeline_type": "Bronze Ingestion Only",
            "records_dumped_to_bronze.metrics": total_ingested,
            "message": f"{total_ingested} metrics successfully archived. Curated coins/prices tables were not affected.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("CMC ingestion failed")
        raise HTTPException(status_code=500, detail=f"CMC Ingestion Failed: {str(e)}")


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
