import sys
import os
import multiprocessing
from sqlalchemy.orm import Session

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import utils.analysis_helpers as analysis_helpers
from app.models.chromosome import Chromosome
from analysis.parallel_utils import cpg_worker

def calculate_cpg_frequency_per_chromosome(db: Session = None):
    def _calculate(db_session: Session):
        print("Calculating CpG dinucleotide frequency (Parallel Optimized)...")
        
        # Fetch IDs only
        chrom_ids = [c.id for c in db_session.query(Chromosome.id).filter(Chromosome.name != "chrM").all()] # Exclude chrM if special handling needed, or include. worker handles it.
        # Usually chrM is small, let's include all.
        chrom_ids = [c.id for c in db_session.query(Chromosome.id).all()]

        # Use Pool
        # Number of processes = CPU count (usually 4-8 on dev machines)
        pool_size = min(len(chrom_ids), multiprocessing.cpu_count())
        
        cpg_frequency_results = {}
        
        print(f"  Spawning {pool_size} worker processes...")
        with multiprocessing.Pool(pool_size) as pool:
            results = pool.map(cpg_worker, chrom_ids)
            
            for res in results:
                if res:
                    name, percentage = res
                    cpg_frequency_results[name] = percentage
                    print(f"  {name}: {percentage:.4f}%")

        analysis_helpers.upsert_statistic(db_session, "cpg_frequency_per_chromosome", cpg_frequency_results)
        print("Successfully calculated and stored CpG frequency per chromosome.")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    # Multiprocessing needs this on Windows/MacOS
    multiprocessing.set_start_method("spawn", force=True)
    calculate_cpg_frequency_per_chromosome()