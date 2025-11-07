import pandas as pd
from sqlalchemy.orm import Session
import os

import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine
from app.models.chromosome import Chromosome
from app.models.gene import Gene, Base

GTF_FILE_PATH = "Homo_sapiens.GRCh38.115.chr.gtf"
GTF_COLUMNS = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame", "attribute"]

def parse_and_store_gtf():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        print(f"Reading GTF file: {GTF_FILE_PATH}")
        df = pd.read_csv(GTF_FILE_PATH, sep='\t', comment='#', names=GTF_COLUMNS, low_memory=False)
        
        genes_df = df[df["feature"] == "gene"].copy()
        print(f"Found {len(genes_df)} gene entries in file.")

        print("Extracting attributes...")
        # This .str.extract() method is more stable and avoids the numpy error
        genes_df['gene_id'] = genes_df['attribute'].str.extract(r'gene_id "([^"]+)"')
        genes_df['gene_name'] = genes_df['attribute'].str.extract(r'gene_name "([^"]+)"')
        genes_df.dropna(subset=["gene_id"], inplace=True)
        
        print("Checking for existing genes in the database...")
        existing_gene_ids = {g[0] for g in db.query(Gene.gene_id).all()}
        print(f"Found {len(existing_gene_ids)} genes already in the database. Will only add new ones.")
        
        chromosomes_map = {c.name: c.id for c in db.query(Chromosome).all()}
        
        genes_to_add = []
        for index, row in genes_df.iterrows():
            if row["gene_id"] in existing_gene_ids:
                continue

            chromosome_name = "chr" + str(row["seqname"])
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
                genes_to_add.append(new_gene)
        
        if genes_to_add:
            print(f"Adding {len(genes_to_add)} new genes to the database...")
            db.bulk_save_objects(genes_to_add)
            db.commit()
            print("Successfully stored new genes.")
        else:
            print("No new genes to add.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    parse_and_store_gtf()