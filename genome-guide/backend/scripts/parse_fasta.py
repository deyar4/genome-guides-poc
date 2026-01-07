import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from Bio import SeqIO
import utils.analysis_helpers as analysis_helpers
from app.models.chromosome import Chromosome

FASTA_FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else "uploads/hg38.fa"

def load_fasta_to_db(file_path, db: Session = None):
    print(f"Loading FASTA: {file_path}")
    
    def _process_fasta(db_session: Session):
        try:
            # Stream records one by one
            for record in SeqIO.parse(file_path, "fasta"):
                chrom_name = record.id
                seq = str(record.seq)
                length = len(seq)
                
                existing_chromosome = db_session.query(Chromosome).filter(Chromosome.name == chrom_name).first()
                
                if existing_chromosome:
                    existing_chromosome.sequence = seq
                    existing_chromosome.length = length
                    print(f"  Updated {chrom_name} (Length: {length})")
                else:
                    new_chromosome = Chromosome(name=chrom_name, sequence=seq, length=length)
                    db_session.add(new_chromosome)
                    print(f"  Added {chrom_name} (Length: {length})")
                
                # Commit after each chromosome to free memory (if SQLAlchemy session manages it well)
                # and to show progress
                db_session.commit()
            
            print("Successfully loaded FASTA sequences.")
        except Exception as e:
            print(f"An error occurred: {e}")
            db_session.rollback()
            raise

    if db:
        _process_fasta(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _process_fasta(session)

if __name__ == "__main__":
    load_fasta_to_db(FASTA_FILE_PATH)