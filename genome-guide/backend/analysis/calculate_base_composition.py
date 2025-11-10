from collections import Counter
from sqlalchemy.orm import Session
import json
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal
from app.models.chromosome import Chromosome
from app.models.statistic import GenomeStatistic
from scripts.parse_fasta import upsert_statistic # We can reuse our helper function

def calculate_base_composition():
    db: Session = SessionLocal()
    print("Calculating base composition from sequences in the database...")
    
    nuclear_counts = Counter()
    mitochondrial_counts = Counter()

    try:
        chromosomes = db.query(Chromosome).all()
        if not chromosomes:
            print("No chromosome sequences found in the database. Please run the FASTA parser first.")
            return

        for chrom in chromosomes:
            base_counts = Counter(chrom.sequence.upper())
            if chrom.name == "chrM":
                mitochondrial_counts.update(base_counts)
            else:
                nuclear_counts.update(base_counts)
        
        # Upsert the results
        upsert_statistic(db, "nuclear_base_composition", json.loads(json.dumps(dict(nuclear_counts))))
        upsert_statistic(db, "mitochondrial_base_composition", json.loads(json.dumps(dict(mitochondrial_counts))))
        
        db.commit()
        print("Successfully calculated and stored base composition.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    calculate_base_composition()