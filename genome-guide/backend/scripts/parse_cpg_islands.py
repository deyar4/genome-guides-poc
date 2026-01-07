import os
import sys
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.chromosome import Chromosome
from app.models.cpg_island import CpgIsland
import utils.analysis_helpers as analysis_helpers

# UCSC cpgIslandExt columns:
COLUMNS = ["bin", "chrom", "chromStart", "chromEnd", "name", "length", "cpgNum", "gcNum", "perGc", "perCpg"]

def load_cpg_islands(file_path, db: Session = None):
    print(f"Reading CpG islands file: {file_path}")
    
    if not os.path.exists(file_path):
        print(f"Warning: File {file_path} not found. Skipping CpG island loading.")
        return

    def _process(db_session: Session):
        try:
            # 1. Optimize SQLite
            db_session.execute(text("PRAGMA synchronous = OFF"))
            db_session.execute(text("PRAGMA journal_mode = MEMORY"))
            
            # 2. Get Chromosome Mapping
            chromosome_map = {c.name: c.id for c in db_session.query(Chromosome.name, Chromosome.id).all()}
            
            # 3. Read Data (Chunked for safety, though CpG files are usually small enough)
            CHUNK_SIZE = 50000 
            total_processed = 0
            
            reader = pd.read_csv(
                file_path, sep='\t', names=COLUMNS, header=None, chunksize=CHUNK_SIZE
            )

            for chunk in reader:
                # Map Chromosome IDs
                chunk['chromosome_id'] = chunk['chrom'].map(chromosome_map)
                
                # Handle missing 'chr' prefix if needed
                mask_missing = chunk['chromosome_id'].isna()
                if mask_missing.any():
                    chunk.loc[mask_missing, 'chromosome_id'] = chunk.loc[mask_missing, 'chrom'].apply(lambda x: chromosome_map.get(f"chr{x}"))
                
                # Drop rows where chromosome not found
                chunk.dropna(subset=['chromosome_id'], inplace=True)
                
                if chunk.empty:
                    continue
                
                # Prepare records
                records = []
                for _, row in chunk.iterrows():
                    records.append({
                        "chromosome_id": int(row['chromosome_id']),
                        "start_pos": row['chromStart'],
                        "end_pos": row['chromEnd'],
                        "name": row['name'],
                        "length": row['length'],
                        "cpg_num": row['cpgNum'],
                        "gc_num": row['gcNum'],
                        "per_gc": row['perGc'],
                        "per_cpg": row['perCpg']
                    })
                
                if records:
                    db_session.bulk_insert_mappings(CpgIsland, records)
                    total_processed += len(records)
            
            db_session.commit()
            print(f"Successfully loaded {total_processed} CpG islands into the database.")

        except Exception as e:
            print(f"An error occurred while parsing CpG islands: {e}")
            db_session.rollback()
            raise

    if db:
        _process(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _process(session)

if __name__ == "__main__":
    cpg_file = sys.argv[1] if len(sys.argv) > 1 else "cpgIslandExt.txt"
    load_cpg_islands(cpg_file)