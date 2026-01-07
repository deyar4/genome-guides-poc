from sqlalchemy.orm import Session
from ..models.telomere import Telomere
from ..models.chromosome import Chromosome
from typing import List, Optional

def get_telomeres_by_chromosome_name(db: Session, chromosome_name: str) -> List[Telomere]:
    """
    Retrieve all telomere records for a given chromosome name.
    """
    return db.query(Telomere).filter(Telomere.chromosome_name == chromosome_name).all()

def get_telomere_sequences(db: Session, chromosome_name: str) -> List[dict]:
    """
    Retrieve the sequences of telomeres for a given chromosome.
    Returns a list of dictionaries, each containing telomere details and its sequence.
    """
    telomere_records = get_telomeres_by_chromosome_name(db, chromosome_name)
    if not telomere_records:
        return []
    
    chromosome = db.query(Chromosome).filter(Chromosome.name == chromosome_name).first()
    if not chromosome or not chromosome.sequence:
        return []
    
    results = []
    for telomere in telomere_records:
        start_idx = telomere.start_position - 1
        end_idx = telomere.end_position 
        
        sequence = chromosome.sequence[start_idx:end_idx]
        results.append({
            "chromosome_name": telomere.chromosome_name,
            "start_position": telomere.start_position,
            "end_position": telomere.end_position,
            "length": telomere.length,
            "sequence": sequence
        })
    return results