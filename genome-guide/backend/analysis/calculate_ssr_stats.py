import sys, os
from collections import Counter
from sqlalchemy import func

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.analysis_helpers import get_db_session, upsert_statistic
from app.models.repeat import SimpleRepeat

def calculate_ssr_stats():
    db = get_db_session()
    print("Calculating Simple Sequence Repeat (SSR) statistics...")
    
    stats = {
        "overall_counts": {},     # Count by unit size (1, 2, 3...)
        "homopolymers": {},       # Specific breakdown of A, C, G, T repeats
        "dinucleotides": {},      # Specific breakdown of AC, AG, etc.
        "trinucleotides": {},     # Specific breakdown of CAG, etc. (Top 10)
        "total_coverage_bp": 0    # How much of the genome is SSRs?
    }

    try:
        # 1. Get counts by Unit Size (Period)
        # This answers: "How many homopolymers vs dinucleotides?"
        unit_size_counts = db.query(
            SimpleRepeat.unit_size, func.count(SimpleRepeat.id)
        ).group_by(SimpleRepeat.unit_size).all()
        
        for size, count in unit_size_counts:
            stats["overall_counts"][size] = count

        # 2. Get Total Coverage (Sum of lengths)
        total_len = db.query(func.sum(SimpleRepeat.total_length)).scalar()
        stats["total_coverage_bp"] = total_len or 0

        # 3. Get Specific Homopolymer Counts (e.g., Poly-A vs Poly-C)
        homopolymers = db.query(SimpleRepeat.sequence, func.count(SimpleRepeat.id))\
            .filter(SimpleRepeat.unit_size == 1)\
            .group_by(SimpleRepeat.sequence).all()
        stats["homopolymers"] = {seq: count for seq, count in homopolymers}

        # 4. Get Specific Dinucleotide Counts
        dinucleotides = db.query(SimpleRepeat.sequence, func.count(SimpleRepeat.id))\
            .filter(SimpleRepeat.unit_size == 2)\
            .group_by(SimpleRepeat.sequence).all()
        stats["dinucleotides"] = {seq: count for seq, count in dinucleotides}

        # 5. Get Top 20 Trinucleotide Counts (There are too many to show all)
        trinucleotides = db.query(SimpleRepeat.sequence, func.count(SimpleRepeat.id))\
            .filter(SimpleRepeat.unit_size == 3)\
            .group_by(SimpleRepeat.sequence)\
            .order_by(func.count(SimpleRepeat.id).desc())\
            .limit(20).all()
        stats["trinucleotides"] = {seq: count for seq, count in trinucleotides}

        # Store the results
        upsert_statistic(db, "ssr_statistics", stats)
        print("Successfully calculated and stored SSR statistics.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    calculate_ssr_stats()