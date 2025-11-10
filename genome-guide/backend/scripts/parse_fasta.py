import os
from Bio import SeqIO
from sqlalchemy.orm import Session
import json

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine
# Import all models so Base knows about them all
from app.models.chromosome import Chromosome
from app.models.gene import Gene
from app.models.statistic import GenomeStatistic, Base

FASTA_FILE_PATH = "hg38.fa" # Make sure this path is correct

def load_fasta_to_db():
    print("Initializing database and creating all tables...")
    # This creates all tables: chromosomes, genes, genome_stats
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        print(f"Parsing {FASTA_FILE_PATH} and loading sequences into database...")
        for record in SeqIO.parse(FASTA_FILE_PATH, "fasta"):
            if "_" in record.id: # Skip alternate scaffolds
                continue

            existing_chromosome = db.query(Chromosome).filter(Chromosome.name == record.id).first()
            if not existing_chromosome:
                new_chromosome = Chromosome(
                    name=record.id,
                    length=len(record.seq),
                    sequence=str(record.seq.upper()) # Store the sequence
                )
                db.add(new_chromosome)
        
        db.commit()
        print("Successfully loaded all primary chromosome sequences into the database.")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    load_fasta_to_db()















# Old version parsing the data based on what analysis we're doing.



# import os
# from Bio import SeqIO
# from sqlalchemy.orm import Session
# from collections import Counter
# import json

# import sys 
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))

# from app.db.session import SessionLocal, engine
# from app.models.chromosome import Chromosome
# from app.models.gene import Gene    
from app.models.statistic import GenomeStatistic, Base  

# FASTA_FILE_PATH = "hg38.fa"

def upsert_statistic(db: Session, name: str, value: dict):
    existing_stat = db.query(GenomeStatistic).filter(GenomeStatistic.stat_name == name).first()
    if existing_stat:
        existing_stat.stat_value = value
        print(f"Updating statistic: {name}")

    else:
        new_stat = GenomeStatistic(stat_name = name, stat_value = value)
        db.add(new_stat)
        print(f"Creating new statistic: {name}")


# def parse_and_store_fasta():
#     print("Initiallizing database and creating all tables")
#     Base.metadata.create_all(bind=engine)
#     db: Session = SessionLocal()

#     nuclear_counts = Counter()
#     mitochondrial_counts = Counter()

#     try:
#         print(f"Starting to parse FASTA file: {FASTA_FILE_PATH}")
#         records = list(SeqIO.parse(FASTA_FILE_PATH, "fasta"))

#         for record in records:
#             existing_chromosome = db.query(Chromosome).filter(Chromosome.name == record.id).first()
#             if not existing_chromosome:
#                 new_chromosome = Chromosome(name=record.id, length=len(record.seq))
#                 db.add(new_chromosome)

#             seq_upper = record.seq.upper()
#             base_counts = Counter(seq_upper)

#             if record.id == "chrM":
#                 mitochondrial_counts.update(base_counts)
#             elif "_" not in record.id:
#                 nuclear_counts.update(base_counts)

#         print("Committting chromosome lengths...")
#         db.commit()

#         print("Storing base composition statistics...")

#         nuclear_value = json.loads(json.dumps(dict(nuclear_counts)))
#         mitochondrial_value = json.loads(json.dumps(dict(mitochondrial_counts)))

#         upsert_statistic(db, "nuclear_base_composition", nuclear_value)
#         upsert_statistic(db, "mitochondrian_base_composition", mitochondrial_value)

#         db.commit()
#         print("Successfully parsed and stored all data!")

#     except Exception as e:
#         print(f"An error occured: {e}")
#         db.rollback()
#     finally:
#         db.close()
#         print("Database session closed.")

# if __name__ == "__main__":
#     parse_and_store_fasta()
