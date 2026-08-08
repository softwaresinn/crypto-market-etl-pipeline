import logging
from fastapi import APIRouter, HTTPException
from core.config import get_settings
from repositories.silver_repository import insert_silver_binance_future

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/etl", tags=["etl"])



@router.post("/binance-future-pairs/transform")
async def transform_binance_future_pairs():
    try:
    
        insert_silver_binance_future()
        return {
            "status": "success",
            "pipeline_type": "Curated",
            "message": "Binance Future Pairs successfully transformed and inserted into Curated tables were not affected.",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Binance future pairs transformation/insertion Silver Layer failed")
        raise HTTPException(status_code=500, detail=f"Binance Future Pairs Silver Layer Insertion Failed: {str(e)}")
