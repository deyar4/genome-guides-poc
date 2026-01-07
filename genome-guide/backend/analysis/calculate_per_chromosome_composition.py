from collections import Counter
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
import utils.analysis_helpers as analysis_helpers # Import the module
from app.models.chromosome import Chromosome

def calculate_per_chromosome_composition(db: Session = None):

    def _calculate(db_session: Session):
        print("Calculating per-chromosome base composition (Optimized)...")
        
        per_chromosome_composition = {}

        try:
            # 1. Get list of chromosome IDs to iterate one by one
            # This avoids loading all sequences into memory at once
            chrom_ids = db_session.query(Chromosome.id, Chromosome.name).all()
            
            if not chrom_ids:
                print("No chromosome sequences found. Run 'parse_fasta.py' first.")
                return

            for chrom_id, name in chrom_ids:
                if "_" in name:
                    continue
                
                # Fetch sequence for just this chromosome
                chrom = db_session.query(Chromosome.sequence).filter(Chromosome.id == chrom_id).scalar()
                
                if chrom:
                    # Optimized counting using built-in string methods
                    # This is significantly faster than Counter(generator)
                    sequence_upper = chrom.upper()
                    base_counts = {
                        'A': sequence_upper.count('A'),
                        'C': sequence_upper.count('C'),
                        'G': sequence_upper.count('G'),
                        'T': sequence_upper.count('T')
                    }
                    per_chromosome_composition[name] = base_counts
                    print(f"  Processed {name}")
            
            analysis_helpers.upsert_statistic(db_session, "per_chromosome_composition", per_chromosome_composition)
            print("Successfully calculated and stored per-chromosome composition.")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_per_chromosome_composition()