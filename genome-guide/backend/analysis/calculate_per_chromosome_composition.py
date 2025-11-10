from collections import Counter
import sys, os

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.analysis_helpers import get_db_session, upsert_statistic
from app.models.chromosome import Chromosome

def calculate_per_chromosome_composition():
    db = get_db_session()
    print("Calculating per-chromosome base composition...")
    
    # This dictionary will hold the results, e.g., {"chr1": {"A": 123...}, "chr2": {...}}
    per_chromosome_composition = {}

    try:
        # Fetch the name and sequence for all chromosomes
        chromosomes = db.query(Chromosome.name, Chromosome.sequence).all()
        if not chromosomes:
            print("No chromosome sequences found. Run 'parse_fasta.py' first.")
            return

        for name, sequence in chromosomes:
             if sequence: # Ensure sequence is not None
                # We only want primary chromosomes for this stat
                if "_" not in name:
                    base_counts = Counter(sequence.upper())
                    per_chromosome_composition[name] = dict(base_counts)
        
        # Save the entire result as one entry in the stats table
        upsert_statistic(db, "per_chromosome_composition", per_chromosome_composition)
        print("Successfully calculated and stored per-chromosome composition.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    calculate_per_chromosome_composition()