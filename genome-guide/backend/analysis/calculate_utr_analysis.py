import sys
import os
import numpy as np
from scipy.stats import pearsonr

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.gene import Gene
from app.models.exon import Exon
from app.models.utr import Utr
from app.models.chromosome import Chromosome
import utils.analysis_helpers as analysis_helpers

def calculate_utr_analysis(db: Session = None):
    def _calculate(db_session: Session):
        print("Calculating correlation between transcript length and UTR length (optimized)...")
        
        # We need to import Chromosome to avoid mapper errors in some environments
        # but we don't need to query it.
        
        # 1. Calculate Total Exon Length per Gene using SQL aggregation
        print("  Querying exon lengths...")
        exon_lengths = db_session.query(
            Exon.gene_id,
            func.sum(Exon.end_pos - Exon.start_pos + 1).label("total_exon_len")
        ).group_by(Exon.gene_id).all()
        exon_map = {gid: length for gid, length in exon_lengths}

        # 2. Calculate Total UTR Length per Gene using SQL aggregation
        print("  Querying UTR lengths...")
        utr_lengths_raw = db_session.query(
            Utr.gene_id,
            func.sum(Utr.end_pos - Utr.start_pos + 1).label("total_utr_len")
        ).group_by(Utr.gene_id).all()
        utr_map = {gid: length for gid, length in utr_lengths_raw}

        # 3. Combine Data
        print("  Combining results...")
        transcript_lengths = []
        utr_lengths = []
        
        # We iterate over genes that have exons (transcripts)
        for gene_id, exon_len in exon_map.items():
            u_len = utr_map.get(gene_id, 0)
            transcript_lengths.append(exon_len)
            utr_lengths.append(u_len)

        correlation = 0.0
        p_value = 1.0
        if len(transcript_lengths) > 1:
            # Check for variance to avoid pearsonr errors
            if len(set(transcript_lengths)) > 1 and len(set(utr_lengths)) > 1:
                correlation, p_value = pearsonr(transcript_lengths, utr_lengths)

        result = {
            "correlation_coefficient": float(correlation),
            "p_value": float(p_value),
            "total_genes_analyzed": len(transcript_lengths),
            "average_transcript_length": float(np.mean(transcript_lengths)) if transcript_lengths else 0,
            "average_utr_length": float(np.mean(utr_lengths)) if utr_lengths else 0
        }

        analysis_helpers.upsert_statistic(db_session, "utr_transcript_correlation", result)
        print(f"Successfully calculated UTR correlation: {correlation:.4f}")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_utr_analysis()