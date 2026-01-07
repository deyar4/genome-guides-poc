import sys
import os
from sqlalchemy import func

# Add the backend directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.models.non_coding_rna import NonCodingRNA
from app.models.chromosome import Chromosome
import utils.analysis_helpers as analysis_helpers

def calculate_rna_distribution(db: Session = None):
    def _calculate(db_session: Session):
        print("Calculating RNA distribution statistics...")
        
        # 1. Counts by Type/Class
        print("  Aggregating counts by RNA class...")
        class_counts = db_session.query(
            NonCodingRNA.rna_class, 
            func.count(NonCodingRNA.id)
        ).group_by(NonCodingRNA.rna_class).all()
        
        class_stats = {cls: count for cls, count in class_counts}
        
        # 2. Counts by Type (detailed)
        print("  Aggregating counts by RNA type...")
        type_counts = db_session.query(
            NonCodingRNA.rna_type, 
            func.count(NonCodingRNA.id)
        ).group_by(NonCodingRNA.rna_type).all()
        
        type_stats = {typ: count for typ, count in type_counts}

        # 3. Density per Chromosome
        print("  Calculating density per chromosome...")
        chromosomes = db_session.query(Chromosome).filter(Chromosome.name != "chrM").all()
        chrom_stats = []
        
        for chrom in chromosomes:
            count = db_session.query(func.count(NonCodingRNA.id)).filter(
                NonCodingRNA.chromosome_id == chrom.id
            ).scalar() or 0
            
            density = count / chrom.length if chrom.length > 0 else 0
            chrom_stats.append({
                "chromosome": chrom.name,
                "count": count,
                "density_per_bp": density,
                "density_per_mb": density * 1_000_000
            })

        result = {
            "counts_by_class": class_stats,
            "counts_by_type": type_stats,
            "chromosome_distribution": chrom_stats,
            "total_rnas": sum(class_stats.values())
        }

        analysis_helpers.upsert_statistic(db_session, "rna_distribution", result)
        print(f"Successfully calculated RNA stats. Total RNAs: {result['total_rnas']}")

    if db:
        _calculate(db)
    else:
        with analysis_helpers.get_db_session() as session:
            _calculate(session)

if __name__ == "__main__":
    calculate_rna_distribution()