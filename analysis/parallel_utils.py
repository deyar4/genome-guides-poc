import os
import sys
import re
from collections import Counter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add backend to path so we can import models
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.config import get_settings
from app.models.chromosome import Chromosome

# Worker setup
def get_db_session():
    settings = get_settings()
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def cpg_worker(chrom_id):
    """
    Worker function to calculate CpG stats for a single chromosome.
    Fetches sequence from DB to avoid serialization overhead.
    """
    db = get_db_session()
    try:
        chrom = db.query(Chromosome.name, Chromosome.sequence).filter(Chromosome.id == chrom_id).first()
        if not chrom or not chrom.sequence:
            return None
        
        name, seq = chrom
        seq_upper = seq.upper()
        
        # 1. Count CpG
        cpg_count = seq_upper.count("CG")
        
        # 2. Count Valid Bases
        n_count = seq_upper.count("N")
        total_valid_bases = len(seq_upper) - n_count
        total_dinucleotides = max(0, total_valid_bases - 1)
        
        if total_dinucleotides > 0:
            percentage = (cpg_count / total_dinucleotides) * 100
            return (name, round(percentage, 4))
        return None
    finally:
        db.close()

def dinucleotide_worker(chrom_id):
    """
    Worker function to calculate Dinucleotide frequency for a single chromosome.
    """
    db = get_db_session()
    try:
        chrom = db.query(Chromosome.name, Chromosome.sequence).filter(Chromosome.id == chrom_id).first()
        if not chrom or not chrom.sequence:
            return None
        
        name, seq = chrom
        seq_upper = seq.upper()
        
        counts = Counter()
        bases = ['A', 'C', 'G', 'T']
        
        # Hybrid Counting Strategy
        for b1 in bases:
            for b2 in bases:
                pair = b1 + b2
                if b1 != b2:
                    # Non-overlapping case: "CG" in "CGCG" -> 2. str.count is accurate.
                    counts[pair] += seq_upper.count(pair)
                else:
                    # Overlapping case: "AA" in "AAAA" -> 3. str.count gives 2.
                    # Use Regex for these 4 cases only.
                    # len(re.findall(r'(?=(AA))', seq))
                    # This is much faster than running regex for all 16.
                    counts[pair] += len(re.findall(f'(?=({pair}))', seq_upper))
        
        return counts
    finally:
        db.close()
