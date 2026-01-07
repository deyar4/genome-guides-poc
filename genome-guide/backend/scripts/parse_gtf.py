import os
import sys
import re
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.models.chromosome import Chromosome
from app.models.gene import Gene
from app.models.exon import Exon
from app.models.utr import Utr
import utils.analysis_helpers as analysis_helpers

GTF_FILE_PATH = sys.argv[1] if len(sys.argv) > 1 else "Homo_sapiens.GRCh38.115.chr.gtf"

def load_gtf_to_db(file_path, db: Session = None):
    print(f"Reading GTF file: {file_path} (Optimized Chunked Processing)...")

    def _process_gtf(db_session: Session):
        try:
            # 1. Optimize SQLite
            db_session.execute(text("PRAGMA synchronous = OFF"))
            db_session.execute(text("PRAGMA journal_mode = MEMORY"))
            
            # 2. Get Chromosome Mapping
            chromosome_map = {c.name: c.id for c in db_session.query(Chromosome.name, Chromosome.id).all()}
            alt_chromosome_map = {c.name.replace('chr', ''): c.id for c in db_session.query(Chromosome.name, Chromosome.id).all()}
            
            CHUNK_SIZE = 1_000_000 
            total_processed = 0
            processed_gene_ids = set() # Track inserted gene_ids to prevent duplicates
            
            # Regex for fast extraction
            gene_id_pattern = r'gene_id "([^"].*?)"'
            gene_name_pattern = r'gene_name "([^"].*?)"'

            reader = pd.read_csv(
                file_path,
                sep='\t',
                comment='#',
                header=None,
                names=[
                    "seqname", "source", "feature", "start", "end",
                    "score", "strand", "frame", "attribute"
                ],
                chunksize=CHUNK_SIZE,
                low_memory=False
            )

            for chunk in reader:
                # Extract gene_id for ALL rows in chunk (vectorized)
                chunk['gene_id'] = chunk['attribute'].str.extract(gene_id_pattern)
                
                # Filter subsets
                genes_df = chunk[chunk["feature"] == "gene"].copy()
                exons_df = chunk[chunk["feature"] == "exon"].copy()
                utrs_df = chunk[chunk["feature"].str.contains("utr", case=False, na=False)].copy()

                # --- A. Process Genes ---
                if not genes_df.empty:
                    # Deduplicate within the current chunk first
                    genes_df.drop_duplicates(subset=['gene_id'], inplace=True)
                    
                    # Filter out genes we've already seen globally
                    if processed_gene_ids:
                        genes_df = genes_df[~genes_df['gene_id'].isin(processed_gene_ids)]
                    
                    if not genes_df.empty:
                        genes_df['gene_name'] = genes_df['attribute'].str.extract(gene_name_pattern)
                        
                        # Map seqname to chrom_id
                        genes_df['seqname_str'] = genes_df['seqname'].astype(str)
                        
                        # Create a map for this chunk's seqnames
                        unique_seqnames = genes_df['seqname_str'].unique()
                        chunk_chrom_map = {}
                        for s in unique_seqnames:
                            if s in chromosome_map:
                                chunk_chrom_map[s] = chromosome_map[s]
                            elif f"chr{s}" in chromosome_map:
                                 chunk_chrom_map[s] = chromosome_map[f"chr{s}"]
                            elif s in alt_chromosome_map:
                                 chunk_chrom_map[s] = alt_chromosome_map[s]
                        
                        # Map IDs
                        genes_df['chromosome_id'] = genes_df['seqname_str'].map(chunk_chrom_map)
                        genes_df.dropna(subset=['chromosome_id'], inplace=True)
                        
                        # Prepare dictionaries for bulk insert
                        gene_records = []
                        genes_df.dropna(subset=['gene_id'], inplace=True) # Ensure gene_id is present
                        
                        for _, row in genes_df.iterrows():
                            gene_records.append({
                                "chromosome_id": int(row['chromosome_id']),
                                "gene_id": row['gene_id'],
                                "gene_name": row['gene_name'],
                                "start_pos": row['start'],
                                "end_pos": row['end'],
                                "strand": row['strand']
                            })
                        
                        if gene_records:
                            # Use INSERT OR IGNORE to handle duplicates gracefully (SQLite specific optimization)
                            # This bypasses the need for complex pre-filtering of cross-chunk duplicates
                            stmt = Gene.__table__.insert().prefix_with("OR IGNORE")
                            db_session.execute(stmt, gene_records)
                            
                            # Flush not needed strictly for ID generation if we don't use the IDs immediately in this block for genes
                            # But we need IDs for Exon mapping below.
                            # Querying DB for IDs is safer after insert.
                            db_session.flush()

                # --- Map Gene IDs to DB IDs ---
                # We need the DB IDs (integers) for the exons and UTRs
                # Optimization: Query only the gene_ids present in this chunk's exons/utrs
                needed_gene_ids = set(exons_df['gene_id']).union(set(utrs_df['gene_id']))
                if needed_gene_ids:
                    # Fetch mapping from DB
                    # Chunking the IN clause if too large
                    needed_list = list(needed_gene_ids)
                    gene_id_map = {}
                    
                    # SQLite limit for variables is usually 999 or 32000. 
                    # SQLAlchemy handles this but safer to chunk manually or assume flush worked
                    
                    # Query batches
                    BATCH = 5000
                    for i in range(0, len(needed_list), BATCH):
                        batch_ids = needed_list[i:i+BATCH]
                        results = db_session.query(Gene.gene_id, Gene.id).filter(Gene.gene_id.in_(batch_ids)).all()
                        for gid, db_id in results:
                            gene_id_map[gid] = db_id

                    # --- B. Process Exons ---
                    if not exons_df.empty:
                        exons_df['gene_db_id'] = exons_df['gene_id'].map(gene_id_map)
                        exons_df.dropna(subset=['gene_db_id'], inplace=True)
                        
                        exon_records = exons_df[[ 
                            'gene_db_id', 'start', 'end'
                        ]].rename(columns={
                            'gene_db_id': 'gene_id', 'start': 'start_pos', 'end': 'end_pos'
                        }).to_dict('records')
                        
                        if exon_records:
                            db_session.bulk_insert_mappings(Exon, exon_records)

                    # --- C. Process UTRs ---
                    if not utrs_df.empty:
                        utrs_df['gene_db_id'] = utrs_df['gene_id'].map(gene_id_map)
                        utrs_df.dropna(subset=['gene_db_id'], inplace=True)
                        
                        # Add utr_type
                        utr_records = []
                        for _, row in utrs_df.iterrows():
                            utr_records.append({
                                "gene_id": int(row['gene_db_id']),
                                "start_pos": row['start'],
                                "end_pos": row['end'],
                                "utr_type": row['feature']
                            })
                        
                        if utr_records:
                            db_session.bulk_insert_mappings(Utr, utr_records)
                
                db_session.commit()
                total_processed += len(chunk)
                print(f"  Processed {total_processed:,} lines...")

            print("Successfully loaded all features from GTF.")

        except Exception as e:
            print(f"An error occurred during GTF parsing: {e}")
            db_session.rollback()
            raise

    if db:
        _process_gtf(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _process_gtf(session)

if __name__ == "__main__":
    load_gtf_to_db(GTF_FILE_PATH)
