from fastapi import APIRouter
from .endpoints import chromosomes, genes

api_router = APIRouter()
api_router.include_router(chromosomes.router, prefix="/chromosomes", tags=["chromosomes"])
api_router.include_router(genes.router, prefix="/genes", tags=["genes"])