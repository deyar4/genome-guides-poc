import pandas as pd
from sqlalchemy.orm import Session
import re
import os

from app.db.session import SessionLocal, engine
from app.models.chromosome import Chromosome
from app.models.gene import Gene, Base 

# --- Configuration ---
GTF_FILE_PATH = "Homo_sapiens.GRCh38.115.chr.gtf"
GTF_COLUMNS = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame", "attribute"]

def parse_attributes(attribute_str: str):
    """Parses the GTF attribute string and extracts gene_id and gene_name."""
    gene_id_match = re.search(r'gene_id "([^"]+)"', attribute_str)
    gene_name_match = re.search(r'gene_name "([^"]+)"', attribute_str)
    
    gene_id = gene_id_match.group(1) if gene_id_match else None
    gene_name = gene_name_match.group(1) if gene_name_match else None
    
    return gene_id, gene_name

def parse_and_store_gtf():
    """Parses a GTF file and stores gene data in the database."""
    print("Initializing database...")
    # This will create both 'chromosomes' and 'genes' tables if they don't exist
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

        # Parse the 'attribute' column to get gene_id and gene_name
        attributes_parsed = genes_df["attribute"].apply(parse_attributes)
        genes_df["gene_id"] = [attr[0] for attr in attributes_parsed]
        genes_df["gene_name"] = [attr[1] for attr in attributes_parsed]
        
        # Drop rows where gene_id could not be parsed
        genes_df.dropna(subset=["gene_id"], inplace=True)

        print("Storing genes in the database...")
        # Get chromosome '22' from our database to link genes to it
        chromosome_obj = db.query(Chromosome).filter(Chromosome.name == "chr22").one_or_none()
        if not chromosome_obj:
            print("ERROR: Chromosome 'chr22' not found in the database. Please run the FASTA parser first.")
            return

        for index, row in genes_df.iterrows():
            new_gene = Gene(
                gene_id=row["gene_id"],
                gene_name=row["gene_name"],
                chromosome_id=chromosome_obj.id, # Link to the chromosome's primary key
                start_pos=row["start"],
                end_pos=row["end"],
                strand=row["strand"]
            )
            db.add(new_gene)
        
        db.commit()
        print(f"Successfully stored {len(genes_df)} genes for chromosome {chromosome_obj.name}.")

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