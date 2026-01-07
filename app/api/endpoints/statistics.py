from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...schemas.statistic import Statistic
from ..dependencies import get_db
from ...crud import crud_statistic # Import the new crud_statistic

router = APIRouter()

@router.get("/{stat_name}", response_model=Statistic)
def get_statistic(stat_name: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific genome statistic by name.
    """
    # Use the crud_statistic module
    stat = crud_statistic.get_statistic_by_name(db=db, stat_name=stat_name)
    if stat is None:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return stat