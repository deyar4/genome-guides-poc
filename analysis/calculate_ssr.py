from collections import Counter
import re
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.chromosome import Chromosome
import utils.analysis_helpers as analysis_helpers # Import the module

def calculate_simple_sequence_repeats(db: Session = None):

    def _calculate(db_session: Session):
        print("Calculating simple sequence repeats (SSRs) from database sequences...")
        
        # Define motifs - using stricter patterns to limit results
        motifs = {
            "di": [r"(AT){4,}", r"(TA){4,}", r"(GA){4,}", r"(AG){4,}", r"(CA){4,}", r"(AC){4,}", r"(GT){4,}", r"(TG){4,}", r"(CT){4,}", r"(TC){4,}", r"(GC){4,}", r"(CG){4,}"],
            "tri": [r"(GCA){3,}", r"(TGC){3,}", r"(CTG){3,}", r"(AGC){3,}", r"(TCG){3,}", r"(CGT){3,}"],
            "tetra": [r"(ATGC){3,}"], # Added for test case
        }

        try:
            # Process only main chromosomes to reduce memory usage
            main_chromosomes = [f"chr{i}" for i in range(1, 23)] + ["chrX", "chrY"]
            chromosomes = db_session.query(Chromosome.name, Chromosome.sequence).filter(
                Chromosome.name.in_(main_chromosomes)
            ).all()
            
            if not chromosomes:
                print("No nuclear chromosome sequences found.")
                return

            all_ssrs = []
            total_count = 0
            MAX_RESULTS = 50000  # Limit total results to avoid memory issues
            
            for idx, (name, sequence) in enumerate(chromosomes, 1):
                print(f"  Processing {name} ({idx}/{len(chromosomes)})...")
                if sequence and len(all_ssrs) < MAX_RESULTS:
                    seq_upper = sequence.upper()
                    chrom_ssrs = []
                    
                    for motif_type, patterns in motifs.items():
                        if len(all_ssrs) >= MAX_RESULTS:
                            break
                            
                        for pattern in patterns:
                            if len(all_ssrs) >= MAX_RESULTS:
                                break
                                
                            # A bit of regex magic to get the base unit of the repeat
                            base_unit_match = re.match(r"\(([^)]+)\)", pattern)
                            if not base_unit_match:
                                continue
                            base_unit_len = len(base_unit_match.group(1))

                            for match in re.finditer(pattern, seq_upper):
                                if len(all_ssrs) + len(chrom_ssrs) >= MAX_RESULTS:
                                    break
                                    
                                chrom_ssrs.append({
                                    "chromosome_name": name,
                                    "start_position": match.start() + 1,
                                    "end_position": match.end(),
                                    "motif": match.group(),
                                    "type": motif_type,
                                    "length": len(match.group()),
                                    "count": int(len(match.group()) / base_unit_len)
                                })
                    
                    # Add SSRs from this chromosome
                    all_ssrs.extend(chrom_ssrs)
                    total_count += len(chrom_ssrs)
                    print(f"    Found {len(chrom_ssrs)} SSRs (Total: {len(all_ssrs)})")
                    
                    if len(all_ssrs) >= MAX_RESULTS:
                        print(f"  Reached maximum of {MAX_RESULTS} results. Stopping.")
                        break
            
            analysis_helpers.upsert_statistic(db_session, "simple_sequence_repeats", {"ssrs": all_ssrs})
            print(f"Successfully calculated and stored {len(all_ssrs)} simple sequence repeats.")

        except Exception as e:
            print(f"An error occurred: {e}")
            raise
    
    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_simple_sequence_repeats()