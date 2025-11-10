import sys, os
from collections import Counter

# Add the parent directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.analysis_helpers import get_db_session, upsert_statistic
from app.models.chromosome import Chromosome

def calculate_cpg_frequency_per_chromosome():
    db = get_db_session()
    print("Calculating CpG dinucleotide frequency for each chromosome...")
    
    cpg_frequency_results = {}

    try:
        # --- THIS IS THE CORRECTED QUERY ---
        # We fetch all chromosomes and filter in Python, just like the other scripts
        chromosomes = db.query(Chromosome.name, Chromosome.sequence).all()
        # ------------------------------------
        
        if not chromosomes:
            print("No chromosome sequences found. This should not happen if parse_fasta ran.")
            return

        for name, sequence in chromosomes:
            # We add the filter here in Python, which is more reliable
            if not sequence or "_" in name:
                continue

            seq_upper = sequence.upper()
            cpg_count = 0
            total_dinucleotides = 0
            
            for i in range(len(seq_upper) - 1):
                dinucleotide = seq_upper[i:i+2]
                if 'N' in dinucleotide:
                    continue
                
                if dinucleotide == 'CG':
                    cpg_count += 1
                
                total_dinucleotides += 1

            if total_dinucleotides > 0:
                cpg_percentage = (cpg_count / total_dinucleotides) * 100
                cpg_frequency_results[name] = round(cpg_percentage, 4)
        
        upsert_statistic(db, "cpg_frequency_per_chromosome", cpg_frequency_results)
        print("Successfully calculated and stored CpG frequency per chromosome.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    calculate_cpg_frequency_per_chromosome()