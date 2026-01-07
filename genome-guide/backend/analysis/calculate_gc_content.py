from collections import Counter
import sys, os
import gc

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
import utils.analysis_helpers as analysis_helpers
from app.models.chromosome import Chromosome

def calculate_gc_content_per_chromosome(db: Session = None):

    def _calculate(db_session: Session):
        print("Calculating GC-content for each chromosome (Optimized)...")
        
        gc_content_results = {}

        try:
            # Fetch IDs first to iterate one by one
            chrom_ids = db_session.query(Chromosome.id, Chromosome.name).all()

            for chrom_id, name in chrom_ids:
                if "_" in name:
                    continue

                sequence = db_session.query(Chromosome.sequence).filter(Chromosome.id == chrom_id).scalar()
                
                if not sequence:
                    continue

                seq_upper = sequence.upper()
                del sequence # Free memory
                
                # Optimize: Use Counter directly on the string
                # This is much faster than (c for c in seq if c in 'ACGT')
                base_counts = Counter(seq_upper)
                
                gc_count = base_counts.get('G', 0) + base_counts.get('C', 0)
                # Count total A, C, G, T (ignore Ns)
                total_bases = (base_counts.get('A', 0) + 
                             base_counts.get('T', 0) + 
                             gc_count)

                if total_bases > 0:
                    gc_percentage = (gc_count / total_bases) * 100
                    gc_content_results[name] = round(gc_percentage, 2)
                    print(f"  {name}: {gc_percentage:.2f}%")
                
                del seq_upper
                del base_counts
                gc.collect()
            
            analysis_helpers.upsert_statistic(db_session, "gc_content_per_chromosome", gc_content_results)
            print("Successfully calculated and stored GC-content per chromosome.")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_gc_content_per_chromosome()