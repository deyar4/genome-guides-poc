import sys
import os

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.gene import Gene
from app.models.chromosome import Chromosome
import utils.analysis_helpers as analysis_helpers

def identify_nested_genes(db: Session = None):
    def _calculate(db_session: Session):
        print("Identifying nested genes (optimized: tuple fetch)...")
        
        # Optimization: Query only necessary columns (tuples) instead of full ORM objects
        # 0:id, 1:chromosome_id, 2:start_pos, 3:end_pos, 4:gene_name, 5:gene_id
        genes_data = db_session.query(
            Gene.id, 
            Gene.chromosome_id, 
            Gene.start_pos, 
            Gene.end_pos, 
            Gene.gene_name, 
            Gene.gene_id
        ).all()
        
        nested_pairs = []

        # Group genes by chromosome
        genes_by_chrom = {}
        for g in genes_data:
            chrom_id = g[1]
            if chrom_id not in genes_by_chrom:
                genes_by_chrom[chrom_id] = []
            genes_by_chrom[chrom_id].append(g)

        for chrom_id, chrom_genes in genes_by_chrom.items():
            # Sort genes by start position for optimized spatial search
            # x[2] is start_pos
            chrom_genes.sort(key=lambda x: x[2])
            
            n = len(chrom_genes)
            for i in range(n):
                g_outer = chrom_genes[i]
                outer_end = g_outer[3]
                
                # Check subsequent genes
                for j in range(i + 1, n):
                    g_inner = chrom_genes[j]
                    inner_start = g_inner[2]
                    inner_end = g_inner[3]
                    
                    # If the next gene starts after the current gene ends, 
                    # it cannot be nested inside the current gene.
                    if inner_start > outer_end:
                        break
                    
                    # Check if g_inner is entirely within g_outer
                    if inner_end <= outer_end:
                        nested_pairs.append({
                            "inner_gene": g_inner[4] or g_inner[5], # gene_name or gene_id
                            "outer_gene": g_outer[4] or g_outer[5], # gene_name or gene_id
                            "chromosome_id": chrom_id
                        })

        result = {
            "total_nested_pairs": len(nested_pairs),
            "nested_pairs": nested_pairs
        }

        analysis_helpers.upsert_statistic(db_session, "nested_genes_statistics", result)
        print(f"Successfully identified {len(nested_pairs)} nested gene pairs.")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    identify_nested_genes()