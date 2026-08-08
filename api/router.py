from fastapi import APIRouter 
from api.routes import binance_ingestion,cmc_ingestion


api_router=APIRouter()

api_router.include_router(binance_ingestion.router)
api_router.include_router(cmc_ingestion.router)
