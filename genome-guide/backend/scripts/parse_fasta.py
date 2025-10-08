import os
from Bio import SeqIO
from sqlalchemy.orm import Session
from collections import Counter
import json

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine
# Import all our models so the Base is aware of them
from app.models.chromosome import Chromosome
from app.models.gene import Gene
from app.models.statistic import GenomeStatistic, Base

FASTA_FILE_PATH = "hg38.fa" # Make sure this path is correct

def parse_and_store_fasta():
    print("Initializing database and creating all tables...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    # Initialize counters
    nuclear_counts = Counter()
    mitochondrial_counts = Counter()
    
    try:
        print(f"Starting to parse FASTA file: {FASTA_FILE_PATH}")
        records = list(SeqIO.parse(FASTA_FILE_PATH, "fasta"))
        
        for record in records:
            seq_upper = record.seq.upper()
            base_counts = Counter(seq_upper)
            
            # Store chromosome length (as before)
            existing_chromosome = db.query(Chromosome).filter(Chromosome.name == record.id).first()
            if not existing_chromosome:
                new_chromosome = Chromosome(name=record.id, length=len(record.seq))
                db.add(new_chromosome)

            # Separate mitochondrial and nuclear chromosomes
            if record.id == "chrM":
                mitochondrial_counts.update(base_counts)
            elif "_" not in record.id: # Filter out alternate scaffolds
                nuclear_counts.update(base_counts)
        
        print("Committing chromosome lengths...")
        db.commit()

        # --- Store the new statistics ---
        print("Storing base composition statistics...")
        # Nuclear
        db.merge(GenomeStatistic(
            stat_name="nuclear_base_composition",
            stat_value=json.loads(json.dumps(dict(nuclear_counts)))
        ))
        # Mitochondrial
        db.merge(GenomeStatistic(
            stat_name="mitochondrial_base_composition",
            stat_value=json.loads(json.dumps(dict(mitochondrial_counts)))
        ))

        db.commit()
        print("Successfully parsed and stored all data!")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    parse_and_store_fasta()