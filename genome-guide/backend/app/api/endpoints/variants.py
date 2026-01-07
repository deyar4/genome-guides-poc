from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ...schemas import variant as variant_schemas
from ...crud import crud_variant
from ..dependencies import get_db

router = APIRouter()

@router.post("/", response_model=variant_schemas.VariantOut, status_code=status.HTTP_201_CREATED)
def create_variant(variant: variant_schemas.VariantCreate, db: Session = Depends(get_db)):
    db_variant = crud_variant.get_variant_by_rsid(db, rsid=variant.rsid)
    if db_variant:
        raise HTTPException(status_code=400, detail="Variant with this RSID already exists")
    return crud_variant.create_variant(db=db, variant=variant)

@router.get("/", response_model=List[variant_schemas.VariantOut])
def read_variants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    variants = crud_variant.get_variants(db, skip=skip, limit=limit)
    return variants

@router.get("/{rsid}", response_model=variant_schemas.VariantOut)
def read_variant(rsid: str, db: Session = Depends(get_db)):
    db_variant = crud_variant.get_variant_by_rsid(db, rsid=rsid)
    if db_variant is None:
        raise HTTPException(status_code=404, detail="Variant not found")
    return db_variant