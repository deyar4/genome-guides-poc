from collections import Counter
import sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.analysis_helpers import get_db_session, upsert_statistic
from app.models.chromosome import Chromosome

def calculate_dinucleotide_frequency():
    db = get_db_session()
    print("Calculating dinucleotide frequencies from database sequences...")
    
    dinucleotide_counts = Counter()

    try:
        chromosomes = db.query(Chromosome.sequence).filter(Chromosome.name != "chrM").all()
        if not chromosomes:
            print("No nuclear chromosome sequences found.")
            return

        for (sequence,) in chromosomes: # Unpacking the tuple
             if sequence: # Ensuring sequence is not None
                seq_upper = sequence.upper()
                for i in range(len(seq_upper) - 1):
                    dinucleotide = seq_upper[i:i+2]
                    if 'N' not in dinucleotide:
                        dinucleotide_counts[dinucleotide] += 1
        
        upsert_statistic(db, "dinucleotide_frequency", dict(dinucleotide_counts))
        print("Successfully calculated and stored dinucleotide frequencies.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    calculate_dinucleotide_frequency()