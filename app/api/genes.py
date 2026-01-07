# backend/app/api/genes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services import gene_service
from ..schemas import GeneOut
from ..schemas import Gene, GeneSearchResponse

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{symbol}", response_model=GeneOut)
def get_gene(symbol: str, db: Session = Depends(get_db)):
    gene = gene_service.get_or_fetch_gene(db, symbol)
    if not gene:
        raise HTTPException(status_code=404, detail="Gene not found")
    return GeneOut.from_orm(gene)


@router.get("/search/{query}", response_model=GeneSearchResponse)
def search_genes(query: str, db: Session = Depends(get_db)):
    results = gene_service.search_genes(db, query)
    return {"results": results}