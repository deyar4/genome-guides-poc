import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.centromere import Centromere
import utils.analysis_helpers as analysis_helpers # Import the module

def load_centromeres_to_db():
    print("Initializing database session for centromere loading...")
    with analysis_helpers.get_db_session() as db: # Use the context manager via module

        try:
            # For minimal data, we add a dummy centromere for chr1
            # In a real scenario, this would parse a BED file or similar
            
            # Check if centromere for chr1 already exists to avoid duplicates
            existing_centromere = db.query(Centromere).filter(Centromere.chromosome_name == "chr1").first()
            
            if not existing_centromere:
                # Example for chr1 from minimal.fasta (sequence length 12: ATGCATGCATGC)
                # Centromere in the middle, positions 5 to 8 (1-based)
                new_centromere = Centromere(
                    chromosome_name="chr1",
                    start_position=5,
                    end_position=8,
                    length=(8 - 5 + 1)
                )
                db.add(new_centromere)
                db.commit()
                print(f"Added dummy centromere for chr1: {new_centromere.chromosome_name}:{new_centromere.start_position}-{new_centromere.end_position}")
            else:
                print(f"Centromere for chr1 already exists, skipping.")
            
        except Exception as e:
            print(f"An error occurred during centromere loading: {e}")
            db.rollback()

if __name__ == "__main__":
    load_centromeres_to_db()