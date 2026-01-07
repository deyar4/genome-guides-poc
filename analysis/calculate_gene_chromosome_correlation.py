import sys
import os
import numpy as np
from scipy.stats import pearsonr

# Add the backend directory to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.chromosome import Chromosome
from app.models.gene import Gene
import utils.analysis_helpers as analysis_helpers

def calculate_gene_chromosome_correlation(db: Session = None):
    def _calculate(db_session: Session):
        print("Calculating correlation between gene density and average gene length...")
        
        chromosomes = db_session.query(Chromosome).filter(Chromosome.name != "chrM").all()
        
        chromosome_stats = []
        densities = []
        avg_lengths = []

        for chrom in chromosomes:
            # Get gene count and average length for this chromosome
            # gene_length = end_pos - start_pos + 1
            stats = db_session.query(
                func.count(Gene.id),
                func.avg(Gene.end_pos - Gene.start_pos + 1)
            ).filter(Gene.chromosome_id == chrom.id).first()
            
            gene_count = stats[0] or 0
            avg_length = stats[1] or 0.0
            
            if gene_count > 0:
                density = gene_count / chrom.length
                chromosome_stats.append({
                    "chromosome": chrom.name,
                    "gene_count": gene_count,
                    "density": density,
                    "average_gene_length": avg_length
                })
                densities.append(density)
                avg_lengths.append(avg_length)

        # Calculate Pearson correlation
        correlation = 0.0
        p_value = 1.0
        if len(densities) > 1:
            correlation, p_value = pearsonr(densities, avg_lengths)

        result = {
            "correlation_coefficient": float(correlation),
            "p_value": float(p_value),
            "chromosome_data": chromosome_stats
        }

        analysis_helpers.upsert_statistic(db_session, "gene_density_length_correlation", result)
        print(f"Successfully calculated correlation: {correlation:.4f} (p={p_value:.4f})")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_gene_chromosome_correlation()
