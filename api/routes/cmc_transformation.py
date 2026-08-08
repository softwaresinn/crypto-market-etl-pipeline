import logging
from fastapi import APIRouter, HTTPException
from core.config import get_settings
from repositories.silver_repository import insert_silver_metrics

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/etl", tags=["etl"])



@router.post("/cmc-metrics/transform")
async def transform_binance_future_pairs():
    try:
        insert_silver_metrics()

        return {
            "status": "success",
            "pipeline_type": "Curated",
            "message": "COIN MARKET CAP METRICS successfully transformed and inserted into Curated tables were not affected.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("COIN MARKET CAP METRICS transformation/insertion Silver Layer failed")
        raise HTTPException(status_code=500, detail=f"COIN MARKET CAP METRICS Silver Layer Insertion Failed: {str(e)}")
