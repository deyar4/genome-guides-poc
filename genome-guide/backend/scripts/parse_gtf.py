import pandas as pd
from sqlalchemy.orm import Session
import os

# Adjust path to import from the app directory
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine
from app.models.chromosome import Chromosome
from app.models.gene import Gene, Base # Import Gene and the Base for table creation

# --- Configuration ---
GTF_FILE_PATH = "Homo_sapiens.GRCh38.115.chr.gtf" # Make sure this filename is correct
GTF_COLUMNS = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame", "attribute"]

def parse_and_store_gtf():
    """Parses a GTF file and stores gene data in the database."""
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    print("Database initialized.")

    db: Session = SessionLocal()
    
    try:
        print(f"Reading GTF file: {GTF_FILE_PATH}")
        df = pd.read_csv(
            GTF_FILE_PATH,
            sep='\t',
            comment='#',
            names=GTF_COLUMNS,
            low_memory=False
        )
        
        # Filter for only the 'gene' features
        genes_df = df[df["feature"] == "gene"].copy()
        print(f"Found {len(genes_df)} gene entries to process.")

        # --- REVISED PARSING LOGIC ---
        # Use pandas' efficient .str.extract() instead of .apply()
        # This is faster and avoids the data type issue.
        print("Extracting gene_id and gene_name attributes...")
        genes_df['gene_id'] = genes_df['attribute'].str.extract(r'gene_id "([^"]+)"')
        genes_df['gene_name'] = genes_df['attribute'].str.extract(r'gene_name "([^"]+)"')
        # ----------------------------
        
        # Drop rows where a gene_id could not be found, as it's essential
        genes_df.dropna(subset=["gene_id"], inplace=True)
        print(f"Successfully extracted attributes for {len(genes_df)} genes.")

        print("Storing genes in the database...")
        # Fetch all chromosomes from DB at once for efficiency
        chromosomes_map = {c.name: c.id for c in db.query(Chromosome).all()}
        
        gene_count = 0
        for index, row in genes_df.iterrows():
            # Find the chromosome ID from our map
            chromosome_name = "chr" + row["seqname"]
            chromosome_id = chromosomes_map.get(chromosome_name)

            if chromosome_id:
                new_gene = Gene(
                    gene_id=row["gene_id"],
                    gene_name=row["gene_name"],
                    chromosome_id=chromosome_id,
                    start_pos=row["start"],
                    end_pos=row["end"],
                    strand=row["strand"]
                )
                db.add(new_gene)
                gene_count += 1
            else:
                # This will skip genes on chromosomes not in our DB (like patches/scaffolds)
                pass
        
        print(f"Committing {gene_count} genes to the database...")
        db.commit()
        print("Successfully stored genes.")

    except FileNotFoundError:
        print(f"ERROR: The file was not found at {GTF_FILE_PATH}")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    parse_and_store_gtf()