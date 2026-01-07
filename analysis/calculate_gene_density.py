import sys
import os
import math

# Add the backend directory to sys.path to resolve imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.chromosome import Chromosome
from app.models.gene import Gene
import utils.analysis_helpers as analysis_helpers

BIN_SIZE = 1_000_000  # 1 Mb window

def calculate_gene_density(db: Session = None):
    def _calculate(db_session: Session):
        print(f"Calculating gene density (Window Size: {BIN_SIZE/1_000_000} Mb)...")
        
        chromosomes = db_session.query(Chromosome).filter(Chromosome.name != "chrM").all()
        density_data = {
            "bin_size": BIN_SIZE,
            "data": {}
        }

        for chrom in chromosomes:
            # Create bins
            num_bins = math.ceil(chrom.length / BIN_SIZE)
            bins = [0] * num_bins
            
            # Fetch all gene start positions for this chromosome
            # Optimization: We only need the start position to determine the bin
            gene_starts = db_session.query(Gene.start_pos).filter(Gene.chromosome_id == chrom.id).all()
            
            for (start_pos,) in gene_starts:
                if start_pos is not None:
                    bin_index = min(int(start_pos // BIN_SIZE), num_bins - 1)
                    bins[bin_index] += 1
            
            density_data["data"][chrom.name] = bins
            print(f"  {chrom.name}: {len(gene_starts)} genes processed into {num_bins} bins.")

        analysis_helpers.upsert_statistic(db_session, "gene_density_1mb", density_data)
        print("Successfully calculated and stored gene density.")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_gene_density()
