from fastapi import APIRouter
from .endpoints import chromosomes, genes, statistics

api_router = APIRouter()
api_router.include_router(chromosomes.router, prefix="/chromosomes", tags=["chromosomes"])
api_router.include_router(genes.router, prefix="/genes", tags=["genes"])
api_router.include_router(statistics.router, prefix="/statistics", tags=["statistics"])