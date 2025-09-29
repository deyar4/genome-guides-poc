from sqlalchemy.orm import Session
from ..models import chromosome as model

def get_chromosomes(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all chromosome records from the database.
    """
    return db.query(model.Chromosome).offset(skip).limit(limit).all()