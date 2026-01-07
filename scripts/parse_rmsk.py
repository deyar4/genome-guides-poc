import sys
import os
import pandas as pd
from sqlalchemy.orm import Session

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import get_session_local
from app.models.non_coding_rna import NonCodingRNA
from app.models.chromosome import Chromosome
import utils.analysis_helpers as analysis_helpers

def parse_rmsk(file_path: str):
    print(f"Parsing RepeatMasker file: {file_path}")
    
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} not found.")
        sys.exit(1)

    SessionLocal = get_session_local()
    db: Session = SessionLocal()
    
    # Create chromosome map
    chrom_map = {c.name: c.id for c in db.query(Chromosome).all()}
    
    # RMSK format is usually tab-delimited but sometimes variable whitespace.
    # UCSC Table Browser default download (selected fields) or full download.
    # We'll assume a standard UCSC dump which often has a header.
    # If using the mock created, it has no header. 
    # Let's handle both or assume standard 15+ cols.
    
    # Columns based on standard RMSK track:
    # bin, swScore, milliDiv, milliDel, milliIns, genoName, genoStart, genoEnd, genoLeft, strand, repName, repClass, repFamily, repStart, repEnd, repLeft, id
    
    col_names = [
        "bin", "swScore", "milliDiv", "milliDel", "milliIns", 
        "genoName", "genoStart", "genoEnd", "genoLeft", "strand", 
        "repName", "repClass", "repFamily", "repStart", "repEnd", "repLeft", "id"
    ]
    
    # Determine if there's a header
    # Simple heuristic: read first line
    with open(file_path, 'r') as f:
        first_line = f.readline()
        if first_line.startswith("bin") or "genoName" in first_line:
            header_row = 0
        else:
            header_row = None

    chunk_size = 10000
    rna_classes = ['rRNA', 'tRNA', 'snRNA', 'snoRNA', 'scRNA', 'srpRNA'] # Focus on non-coding RNA
    
    count = 0
    
    try:
        reader = pd.read_csv(
            file_path, 
            sep='\t', 
            header=header_row, 
            names=col_names if header_row is None else None,
            chunksize=chunk_size,
            comment='#'
        )
        
        for chunk in reader:
            chunk_rnas = []
            
            # Filter for RNA
            # repClass is often 'rRNA', 'tRNA', etc.
            # Sometimes SINE/LINE etc are there.
            
            rna_chunk = chunk[chunk['repClass'].isin(rna_classes) | chunk['repClass'].str.contains('RNA', na=False, case=False)]
            # Refine filter: exclude simple repeats if they matched 'RNA' vaguely, but explicitly including expected classes is safer.
            # Actually, standard classes: SINE, LINE, LTR, DNA, Simple_repeat, Low_complexity, Satellite, rRNA, scRNA, snRNA, srpRNA, tRNA, RC, RNA
            
            filtered = chunk[chunk['repClass'].isin(rna_classes)]
            
            for _, row in filtered.iterrows():
                chrom_name = row['genoName']
                if chrom_name not in chrom_map:
                    continue # Skip unknown chromosomes
                
                chunk_rnas.append({
                    "chromosome_id": chrom_map[chrom_name],
                    "start_pos": int(row['genoStart']),
                    "end_pos": int(row['genoEnd']),
                    "strand": row['strand'],
                    "rna_type": row['repClass'], # e.g. tRNA
                    "rna_class": row['repClass'], # same
                    "rna_name": row['repName']    # e.g. tRNA-Ala
                })
            
            if chunk_rnas:
                db.bulk_insert_mappings(NonCodingRNA, chunk_rnas)
                count += len(chunk_rnas)
                db.commit()
                print(f"  Loaded {count} non-coding RNAs...")
                
    except Exception as e:
        print(f"Error parsing RMSK: {e}")
        db.rollback()
    finally:
        db.close()

    print(f"Finished. Total loaded: {count}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python parse_rmsk.py <rmsk_file>")
        sys.exit(1)
    
    parse_rmsk(sys.argv[1])
