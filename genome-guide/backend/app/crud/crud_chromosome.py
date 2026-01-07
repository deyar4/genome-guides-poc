from sqlalchemy.orm import Session
from ..models import chromosome as model
from typing import List, Tuple

def get_chromosomes(db: Session, skip: int = 0, limit: int = 100):
    """
    Retrieve all chromosome records from the database.
    """
    return db.query(model.Chromosome).order_by(model.Chromosome.id).offset(skip).limit(limit).all()

def get_chromosome_lengths(db: Session) -> List[Tuple[str, int]]:
    """
    Retrieve all chromosome names and their lengths from the database.
    """
    return db.query(model.Chromosome.name, model.Chromosome.length).all()