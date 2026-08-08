from fastapi import APIRouter 
from api.routes import etl


api_router=APIRouter()

api_router.include_router(etl.router)
