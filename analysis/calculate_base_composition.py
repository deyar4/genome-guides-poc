from collections import Counter
import sys, os
import gc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
import utils.analysis_helpers as analysis_helpers
from app.models.chromosome import Chromosome

def calculate_base_composition(db: Session = None):
    
    def _calculate(db_session: Session):
        print("Calculating base composition from sequences in the database (Optimized)...")
        
        nuclear_counts = Counter()
        mitochondrial_counts = Counter()

        try:
            chrom_ids = db_session.query(Chromosome.id, Chromosome.name).all()
            
            for chrom_id, name in chrom_ids:
                if "_" in name and name != "chrM": # Skip random contigs to speed up
                    continue
                
                sequence = db_session.query(Chromosome.sequence).filter(Chromosome.id == chrom_id).scalar()
                
                if not sequence:
                    continue
                
                # Optimized: Counter on full string
                base_counts = Counter(sequence.upper())
                del sequence # Free memory immediately
                
                if name == "chrM":
                    mitochondrial_counts.update(base_counts)
                else:
                    nuclear_counts.update(base_counts)
                
                print(f"  Processed {name}")
                del base_counts
                gc.collect()
            
            analysis_helpers.upsert_statistic(db_session, "nuclear_base_composition", dict(nuclear_counts))
            analysis_helpers.upsert_statistic(db_session, "mitochondrial_base_composition", dict(mitochondrial_counts))
            
            print("Successfully calculated and stored base composition.")
        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_base_composition()