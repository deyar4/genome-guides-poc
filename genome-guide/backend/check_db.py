import sys, os
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app.db.session import SessionLocal
from app.models.chromosome import Chromosome

def check_chromosome_data():
    db = SessionLocal()
    print("--- Database Diagnostic Check ---")
    
    try:
        # Try to get the first chromosome from the database
        chromosome = db.query(Chromosome).first()
        
        if not chromosome:
            print("RESULT: FAILURE")
            print("REASON: The 'chromosomes' table is empty.")
            print("ACTION: Make sure 'hg38.fa' is in your 'backend' folder and re-run 'python -m scripts.parse_fasta'.")
            return

        print(f"Found chromosome: {chromosome.name}")
        print(f"Length: {chromosome.length}")
        
        # Check if the sequence column exists and has data
        if not hasattr(chromosome, 'sequence'):
            print("RESULT: FAILURE")
            print("REASON: Your database table is 'chromosomes' is old. It does NOT have the 'sequence' column.")
            print("ACTION: Delete 'genome_guides.db' and re-run 'python -m scripts.parse_fasta'.")
        elif chromosome.sequence is None:
            print("RESULT: FAILURE")
            print("REASON: The 'sequence' column exists but is EMPTY (NULL).")
            print("ACTION: Delete 'genome_guides.db' and re-run 'python -m scripts.parse_fasta'.")
        else:
            print("RESULT: SUCCESS")
            print(f"Sequence: {chromosome.sequence[:50]}...") # Print first 50 chars
            print("REASON: Your database is populated correctly.")
            print("ACTION: The error is in the analysis script. (Please report this).")
            
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        db.close()
        print("--- Check Complete ---")

if __name__ == "__main__":
    check_chromosome_data()