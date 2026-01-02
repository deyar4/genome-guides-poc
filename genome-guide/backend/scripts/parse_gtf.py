import pandas as pd
from sqlalchemy.orm import Session
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine
from app.models.chromosome import Chromosome
from app.models.gene import Gene
from app.models.exon import Exon, Base

GTF_FILE_PATH = "Homo_sapiens.GRCh38.115.chr.gtf"
# We only need specific columns
GTF_COLUMNS = ["seqname", "source", "feature", "start", "end", "score", "strand", "frame", "attribute"]

def parse_and_store_gtf():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        print(f"Reading GTF file: {GTF_FILE_PATH}")
        # Read the file
        df = pd.read_csv(
            GTF_FILE_PATH, 
            sep='\t', 
            comment='#', 
            names=GTF_COLUMNS, 
            low_memory=False,
            usecols=["seqname", "feature", "start", "end", "strand", "attribute"]
        )
        
        # --- PART 1: GENES ---
        print("Processing Genes...")
        genes_df = df[df["feature"] == "gene"].copy()
        
        # Extract attributes
        genes_df['gene_id'] = genes_df['attribute'].str.extract(r'gene_id "([^"]+)"')
        genes_df['gene_name'] = genes_df['attribute'].str.extract(r'gene_name "([^"]+)"')
        genes_df['gene_type'] = genes_df['attribute'].str.extract(r'gene_biotype "([^"]+)"')
        genes_df.dropna(subset=["gene_id"], inplace=True)

        # Check existing genes to avoid duplicates
        existing_gene_ids = {g[0] for g in db.query(Gene.gene_id).all()}
        chromosomes_map = {c.name: c.id for c in db.query(Chromosome).all()}
        
        genes_to_add = []
        for _, row in genes_df.iterrows():
            if row["gene_id"] in existing_gene_ids:
                continue
            
            chrom_name = "chr" + str(row["seqname"])
            chrom_id = chromosomes_map.get(chrom_name)
            
            if chrom_id:
                genes_to_add.append(Gene(
                    gene_id=row["gene_id"],
                    gene_name=row["gene_name"],
                    gene_type=row["gene_type"],
                    chromosome_id=chrom_id,
                    start_pos=row["start"],
                    end_pos=row["end"],
                    strand=row["strand"]
                ))
        
        if genes_to_add:
            print(f"Adding {len(genes_to_add)} new genes...")
            db.bulk_save_objects(genes_to_add)
            db.commit()
        else:
            print("No new genes to add.")

        # --- PART 2: EXONS ---
        print("Processing Exons...")
        # Check if exons are already loaded to save time
        if db.query(Exon).first():
            print("Exons already appear to be loaded. Skipping to avoid duplicates.")
            return

        exons_df = df[df["feature"] == "exon"].copy()
        print(f"Found {len(exons_df)} exons. Extracting attributes...")
        
        exons_df['gene_id'] = exons_df['attribute'].str.extract(r'gene_id "([^"]+)"')
        exons_df['exon_number'] = exons_df['attribute'].str.extract(r'exon_number "(\d+)"')
        exons_df.dropna(subset=["gene_id"], inplace=True)

        # Prepare for bulk insert
        print("Preparing exon data...")
        exons_to_add = []
        
        # We need a set of valid gene_ids to ensure referential integrity
        # (Exons can't point to a gene that doesn't exist in our DB)
        valid_gene_ids = {g[0] for g in db.query(Gene.gene_id).all()}

        count = 0
        for _, row in exons_df.iterrows():
            if row["gene_id"] not in valid_gene_ids:
                continue

            exons_to_add.append(Exon(
                gene_id=row["gene_id"],
                start_pos=row["start"],
                end_pos=row["end"],
                exon_number=int(row["exon_number"]) if pd.notna(row["exon_number"]) else None
            ))
            count += 1
            
            # Batch commit every 100k records to avoid memory issues
            if len(exons_to_add) >= 50000:
                print(f"Committing batch of 50,000 exons...")
                db.bulk_save_objects(exons_to_add)
                db.commit()
                exons_to_add = []

        # Commit remaining
        if exons_to_add:
            db.bulk_save_objects(exons_to_add)
            db.commit()
        
        print(f"Successfully stored {count} exons.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    parse_and_store_gtf()