from sqlalchemy.orm import Session
from ..models.centromere import Centromere
from ..models.chromosome import Chromosome
from typing import Optional

def get_centromere_by_chromosome_name(db: Session, chromosome_name: str) -> Optional[Centromere]:
    """
    Retrieve a centromere record by its chromosome name.
    """
    return db.query(Centromere).filter(Centromere.chromosome_name == chromosome_name).first()

def get_centromere_sequence(db: Session, chromosome_name: str) -> Optional[str]:
    """
    Retrieve the sequence of a centromere for a given chromosome.
    """
    centromere = get_centromere_by_chromosome_name(db, chromosome_name)
    if not centromere:
        return None
    
    chromosome = db.query(Chromosome).filter(Chromosome.name == chromosome_name).first()
    if not chromosome or not chromosome.sequence:
        return None
    
    # Extract the centromere sequence based on its start and end positions
    # Adjust for 0-based indexing if necessary (database typically stores 1-based)
    # Assuming start_position and end_position are 1-based inclusive
    start_idx = centromere.start_position - 1
    end_idx = centromere.end_position # end_position is inclusive in 1-based, slicing is exclusive for end.
    
    return chromosome.sequence[start_idx:end_idx]