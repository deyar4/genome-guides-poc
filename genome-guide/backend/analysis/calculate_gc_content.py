import sys, os
from collections import Counter

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.analysis_helpers import get_db_session, upsert_statistic
from app.models.chromosome import Chromosome

def calculate_gc_content_per_chromosome():
    db = get_db_session()
    print("Calculating GC-content for each chromosome...")
    
    gc_content_results = {}

    try:
        chromosomes = db.query(Chromosome.name, Chromosome.sequence).all()
        if not chromosomes:
            print("No chromosome sequences found. Run 'parse_fasta.py' first.")
            return

        for name, sequence in chromosomes:
            if sequence and "_" not in name:
                # Count only the four main bases
                base_counts = Counter(c for c in sequence.upper() if c in 'ACGT')
                
                gc_count = base_counts.get('G', 0) + base_counts.get('C', 0)
                total_bases = base_counts.get('A', 0) + base_counts.get('T', 0) + gc_count

                if total_bases > 0:
                    gc_percentage = (gc_count / total_bases) * 100
                    gc_content_results[name] = round(gc_percentage, 2)
        
        # Save the final dictionary of { "chr1": 41.77, "chr2": 40.01, ... }
        upsert_statistic(db, "gc_content_per_chromosome", gc_content_results)
        print("Successfully calculated and stored GC-content per chromosome.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    calculate_gc_content_per_chromosome()