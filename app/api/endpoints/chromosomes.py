from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ...schemas import chromosome as chromosome_schemas # Updated import
from ...crud import crud_chromosome
from ..dependencies import get_db

router = APIRouter()

@router.get("/", response_model=List[chromosome_schemas.Chromosome]) # Updated response_model
def read_chromosomes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve all chromosomes from the database.
    """
    chromosomes = crud_chromosome.get_chromosomes(db, skip=skip, limit=limit)
    return chromosomes

@router.get("/lengths", response_model=List[chromosome_schemas.ChromosomeBase])
def read_chromosome_lengths(db: Session = Depends(get_db)):
    """
    Retrieve the name and length of all chromosomes.
    """
    chromosome_lengths = crud_chromosome.get_chromosome_lengths(db)
    # The CRUD function returns a list of tuples (name, length).
    # We need to convert these into ChromosomeBase objects for the response model.
    return [{"name": name, "length": length} for name, length in chromosome_lengths]
