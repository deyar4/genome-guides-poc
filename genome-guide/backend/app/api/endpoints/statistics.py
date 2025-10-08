from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...schemas.statistic import Statistic
from ..dependencies import get_db

router = APIRouter()

@router.get("/{stat_name}", response_model=Statistic)
def get_statistic(stat_name: str, db: Session = Depends(get_db)):
    """
    Retrieve a specific genome statistic by name.
    """
    from ...models.statistic import GenomeStatistic
    stat = db.query(GenomeStatistic).filter(GenomeStatistic.stat_name == stat_name).first()
    if stat is None:
        raise HTTPException(status_code=404, detail="Statistic not found")
    return stat