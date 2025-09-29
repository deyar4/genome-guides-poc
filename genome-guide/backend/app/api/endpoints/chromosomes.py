from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

# Import the CRUD function, schemas, and a dependency to get the DB session
from ... import schemas
from ...crud import crud_chromosome
from ..dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[schemas.Chromosome])
def read_chromosomes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all chromosomes from the database.
    """
    chromosomes = crud_chromosome.get_chromosomes(db, skip=skip, limit=limit)
    return chromosomes
