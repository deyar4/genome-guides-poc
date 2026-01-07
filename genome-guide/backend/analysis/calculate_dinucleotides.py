import sys
import os
import multiprocessing
from collections import Counter
from sqlalchemy.orm import Session

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.analysis_helpers as analysis_helpers
from app.models.chromosome import Chromosome
from analysis.parallel_utils import dinucleotide_worker

def calculate_dinucleotide_frequency(db: Session = None):
    def _calculate(db_session: Session):
        print("Calculating dinucleotide frequency (Parallel Optimized)...")
        
        # Fetch IDs (Filtering out 'chrM' if needed, though worker handles logic)
        chrom_ids = [c.id for c in db_session.query(Chromosome.id).filter(Chromosome.name != "chrM").all()]
        
        pool_size = min(len(chrom_ids), multiprocessing.cpu_count())
        final_counts = Counter()
        
        print(f"  Spawning {pool_size} worker processes...")
        with multiprocessing.Pool(pool_size) as pool:
            results = pool.map(dinucleotide_worker, chrom_ids)
            
            for res in results:
                if res:
                    final_counts.update(res)

        analysis_helpers.upsert_statistic(db_session, "dinucleotide_frequency", dict(final_counts))
        print("Successfully calculated and stored dinucleotide frequencies.")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    multiprocessing.set_start_method("spawn", force=True)
    calculate_dinucleotide_frequency()