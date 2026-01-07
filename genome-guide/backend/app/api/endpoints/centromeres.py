from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from ...schemas.centromere import CentromereSequenceResponse
from ...crud import crud_centromere
from ..dependencies import get_db

router = APIRouter()

@router.get("/{chromosome_name}/sequence", response_model=CentromereSequenceResponse)
def get_centromere_sequence_endpoint(chromosome_name: str, db: Session = Depends(get_db)):
    """
    Retrieve the sequence of the centromere for a given chromosome.
    """
    centromere_record = crud_centromere.get_centromere_by_chromosome_name(db, chromosome_name)
    if not centromere_record:
        raise HTTPException(status_code=404, detail=f"Centromere not found for chromosome {chromosome_name}")
    
    sequence = crud_centromere.get_centromere_sequence(db, chromosome_name)
    if sequence is None:
        raise HTTPException(status_code=404, detail=f"Chromosome sequence or centromere sequence not available for {chromosome_name}")
    
    return CentromereSequenceResponse(
        chromosome_name=centromere_record.chromosome_name,
        start_position=centromere_record.start_position,
        end_position=centromere_record.end_position,
        length=centromere_record.length,
        sequence=sequence
    )