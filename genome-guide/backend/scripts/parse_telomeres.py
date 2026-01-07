import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.telomere import Telomere
import utils.analysis_helpers as analysis_helpers # Import the module

def load_telomeres_to_db():
    """
    Loads dummy telomere data for chr1 into the database.
    In a real-world scenario, this function would parse a BED file or similar
    to extract and store actual telomere locations.
    """
    print("Initializing database session for telomere loading...")
    with analysis_helpers.get_db_session() as db: # Use the context manager

        try:
            # For minimal data, we add dummy telomere entries for chr1
            # In a real scenario, this would parse a BED file or similar.
            
            # Check if telomeres for chr1 already exist to avoid duplicates
            existing_telomeres = db.query(Telomere).filter(Telomere.chromosome_name == "chr1").all()
            
            if not existing_telomeres:
                # Example for chr1 from minimal.fasta (sequence length 12: ATGCATGCATGC)
                # Telomere 1: positions 1 to 4 (1-based)
                new_telomere1 = Telomere(
                    chromosome_name="chr1",
                    start_position=1,
                    end_position=4,
                    length=(4 - 1 + 1)
                )
                db.add(new_telomere1)

                # Telomere 2: positions 9 to 12 (1-based)
                new_telomere2 = Telomere(
                    chromosome_name="chr1",
                    start_position=9,
                    end_position=12,
                    length=(12 - 9 + 1)
                )
                db.add(new_telomere2)

                db.commit() # Commit once at the end
                print(f"Added dummy telomeres for chr1: {new_telomere1.chromosome_name}:{new_telomere1.start_position}-{new_telomere1.end_position} and {new_telomere2.chromosome_name}:{new_telomere2.start_position}-{new_telomere2.end_position}")
            else:
                print(f"Telomeres for chr1 already exist, skipping.")
            
        except Exception as e:
            print(f"An error occurred during telomere loading: {e}")
            db.rollback() # Rollback on error

if __name__ == "__main__":
    load_telomeres_to_db()