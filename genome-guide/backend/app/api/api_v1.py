from fastapi import APIRouter
from .endpoints import chromosomes

api_router = APIRouter()
api_router.include_router(chromosomes.router, prefix="/chromosomes", tags=["chromosomes"])