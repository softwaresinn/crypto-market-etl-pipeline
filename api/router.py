from fastapi import APIRouter 
from api.routes import binance_ingestion, binance_transformation,cmc_ingestion,cmc_transformation


api_router=APIRouter()

api_router.include_router(binance_ingestion.router)
api_router.include_router(cmc_ingestion.router)
api_router.include_router(binance_transformation.router)
api_router.include_router(cmc_transformation.router)