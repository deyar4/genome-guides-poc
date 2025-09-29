from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ... import schemas
from ...crud import crud_gene
from ..dependencies import get_db

router = APIRouter()

@router.get("/search/{query}", response_model=List[schemas.gene.Gene])
def search_for_genes(query: str, db: Session = Depends(get_db)):
    """
    Search for genes by name (case-insensitive).
    """
    genes = crud_gene.search_genes_by_name(db=db, query=query)
    if not genes:
        raise HTTPException(status_code=404, detail="No genes found matching the query")
    return genes

@router.get("/{gene_name}", response_model=schemas.gene.Gene)
def read_gene_by_name(gene_name: str, db: Session = Depends(get_db)):
    """
    Retrieve a single gene by its exact name.
    """
    db_gene = crud_gene.get_gene_by_name(db=db, gene_name=gene_name)
    if db_gene is None:
        raise HTTPException(status_code=404, detail="Gene not found")
    return db_gene