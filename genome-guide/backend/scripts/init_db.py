import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.base_class import Base
from app.db.session import get_engine
from app.models import chromosome, gene, statistic, centromere, telomere, cpg_island, exon, utr, non_coding_rna # Import all models

def init_db(db = None):
    """
    Initializes the database schema by creating all tables defined in the SQLAlchemy models.
    This function should be called once, for example, during application startup or in a Snakemake rule.
    """
    print("Initializing database schema...")
    try:
        if db:
            engine = db.get_bind()
        else:
            engine = get_engine()
        Base.metadata.create_all(bind=engine)
        print("Database schema initialized successfully.")
    except Exception as e:
        print(f"ERROR (init_db.py): An error occurred during database schema initialization: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_db()