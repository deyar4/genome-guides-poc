from sqlalchemy.orm import Session
from ..models.statistic import GenomeStatistic

def get_statistic_by_name(db: Session, stat_name: str):
    return db.query(GenomeStatistic).filter(GenomeStatistic.stat_name == stat_name).first()