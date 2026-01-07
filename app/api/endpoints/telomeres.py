from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ...schemas.telomere import TelomeresResponse, TelomereSequenceResponse
from ...crud import crud_telomere
from ..dependencies import get_db

router = APIRouter()

@router.get("/{chromosome_name}/sequence", response_model=TelomeresResponse)
def get_telomere_sequences_endpoint(chromosome_name: str, db: Session = Depends(get_db)):
    """
    Retrieve the sequences of all telomeres for a given chromosome.
    """
    telomere_sequences_data = crud_telomere.get_telomere_sequences(db, chromosome_name)
    if not telomere_sequences_data:
        raise HTTPException(status_code=404, detail=f"Telomeres not found or no sequence available for chromosome {chromosome_name}")
    
    # crud_telomere.get_telomere_sequences already returns data in a dict format
    # that matches TelomereSequenceResponse, so we just need to wrap it in TelomeresResponse
    return TelomeresResponse(telomeres=[TelomereSequenceResponse(**data) for data in telomere_sequences_data])