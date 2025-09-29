import os
from Bio import SeqIO
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.chromosome import Chromosome
from app.db.session import engine
from app.models.chromosome import Base 

# --- Configuration ---
# The path to FASTA file.
FASTA_FILE_PATH = "hg38.fa"

def init_db():
    """
    Initializes the database and creates tables if they don't exist.
    """
    print("Initializing database and creating tables...")
    #  creating the tables based on models
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")


def parse_and_store_fasta():
    """
    Parses a FASTA file and stores chromosome metadata in the database.
    """
    print(f"Starting to parse FASTA file: {FASTA_FILE_PATH}")

    # Get a new database session
    db: Session = SessionLocal()

    try:
        # Biopython's SeqIO.parse to read the FASTA file
        # This is memory-efficient as it reads one record at a time
        for record in SeqIO.parse(FASTA_FILE_PATH, "fasta"):
            chromosome_name = record.id
            chromosome_length = len(record.seq)

            print(f"Found chromosome: {chromosome_name}, Length: {chromosome_length}")

            # Check if this chromosome already exists in the database
            existing_chromosome = db.query(Chromosome).filter(Chromosome.name == chromosome_name).first()

            if not existing_chromosome:
                # Create a new Chromosome object
                new_chromosome = Chromosome(
                    name=chromosome_name,
                    length=chromosome_length
                )
                # Add it to the session
                db.add(new_chromosome)
                print(f"-> Storing {chromosome_name} in the database.")
            else:
                print(f"-> {chromosome_name} already exists. Skipping.")

        # Commit the transaction to save all changes to the database
        db.commit()
        print("\nSuccessfully parsed and stored all new records!")

    except FileNotFoundError:
        print(f"ERROR: The file was not found at {FASTA_FILE_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Roll back the transaction in case of an error
        db.rollback()
    finally:
        # Always close the session
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    init_db() 
    parse_and_store_fasta()
