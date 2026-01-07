import sys
import os
from collections import defaultdict

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.gene import Gene
from app.models.cpg_island import CpgIsland
from app.models.chromosome import Chromosome
import utils.analysis_helpers as analysis_helpers

def calculate_cpg_association(db: Session = None):
    def _calculate(db_session: Session):
        print("Calculating CpG island association with genes (Optimized: Linear Sweep)...")
        
        # 1. Fetch minimal required data (tuples)
        print("  Fetching data...")
        # (chrom_id, start, end)
        islands_data = db_session.query(CpgIsland.chromosome_id, CpgIsland.start_pos, CpgIsland.end_pos).all()
        genes_data = db_session.query(Gene.chromosome_id, Gene.start_pos, Gene.end_pos).all()
        
        total_islands = len(islands_data)
        if total_islands == 0:
            print("No CpG islands found in database.")
            analysis_helpers.upsert_statistic(db_session, "cpg_island_gene_association", {"total_islands": 0})
            return

        # 2. Group by Chromosome
        islands_by_chrom = defaultdict(list)
        genes_by_chrom = defaultdict(list)

        for chrom_id, start, end in islands_data:
            islands_by_chrom[chrom_id].append((start, end))

        for chrom_id, start, end in genes_data:
            genes_by_chrom[chrom_id].append((start, end))

        overlapping_count = 0
        
        # 3. Process each chromosome
        for chrom_id, islands in islands_by_chrom.items():
            genes = genes_by_chrom.get(chrom_id, [])
            if not genes:
                continue
            
            # Sort by start position for sweep-line
            islands.sort(key=lambda x: x[0])
            genes.sort(key=lambda x: x[0])
            
            num_genes = len(genes)
            gene_idx = 0
            
            for i_start, i_end in islands:
                # Advance gene_idx to the first gene that ends on or after the island starts
                # Since islands are also sorted, we can maintain the gene_idx state 
                # (we don't need to reset it for the next island)
                while gene_idx < num_genes and genes[gene_idx][1] < i_start:
                    gene_idx += 1
                
                # Check for overlaps starting from the current valid gene_idx
                # We look ahead but DO NOT advance gene_idx permanently here (only the while loop does that)
                k = gene_idx
                found_overlap = False
                
                while k < num_genes:
                    g_start, g_end = genes[k]
                    
                    # If this gene starts after the island ends, then NO subsequent gene 
                    # can overlap this island (because genes are sorted by start)
                    if g_start > i_end:
                        break
                    
                    # Intersection check:
                    # We know g_end >= i_start (from the first while loop)
                    # We know g_start <= i_end (from the break condition above)
                    # Therefore, they must overlap.
                    found_overlap = True
                    break 
                    
                    # Note: We don't need to check all overlapping genes, just one is enough.
                
                if found_overlap:
                    overlapping_count += 1

        non_overlapping_count = total_islands - overlapping_count
        
        result = {
            "total_islands": total_islands,
            "associated_with_genes": overlapping_count,
            "non_associated": non_overlapping_count,
            "percentage_associated": (overlapping_count / total_islands) * 100 if total_islands > 0 else 0
        }

        analysis_helpers.upsert_statistic(db_session, "cpg_island_gene_association", result)
        print(f"Successfully calculated CpG association: {result['percentage_associated']:.2f}% associated with genes.")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_cpg_association()
