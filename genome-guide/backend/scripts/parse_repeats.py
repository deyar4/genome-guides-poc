import pandas as pd
from sqlalchemy.orm import Session
import sys, os

# Add the parent directory to the path so we can import 'app'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal, engine
from app.models.repeat import SimpleRepeat, Base

# Configuration
REPEAT_FILE_PATH = "simpleRepeat.txt"

# UCSC simpleRepeat table columns
COLUMN_NAMES = [
    "bin", "chrom", "chromStart", "chromEnd", 
    "name", "period", "copyNum", "consensusSize", 
    "perMatch", "perIndel", "score", "A", "C", "G", "T", "entropy", "sequence"
]

def parse_and_store_repeats():
    print("Initializing database...")
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        print(f"Reading Simple Repeats file: {REPEAT_FILE_PATH}")
        df = pd.read_csv(
            REPEAT_FILE_PATH,
            sep='\t',
            header=None, # We provide our own names
            names=COLUMN_NAMES,
            usecols=["chrom", "chromStart", "chromEnd", "period", "copyNum", "score", "sequence"],
            low_memory=False,
            comment='#' # Skip comment lines if they exist
        )
        
        # --- FIX: Drop the header row if it was read as data ---
        # If the first row's 'copyNum' column is the string "copyNum", drop it.
        if df.iloc[0]['copyNum'] == 'copyNum':
            print("Detected header row in data. Removing it.")
            df = df.iloc[1:]
        
        # Convert copyNum and score to numeric, coercing errors to NaN just in case
        df['copyNum'] = pd.to_numeric(df['copyNum'], errors='coerce')
        df['score'] = pd.to_numeric(df['score'], errors='coerce')
        df['period'] = pd.to_numeric(df['period'], errors='coerce')
        df['chromStart'] = pd.to_numeric(df['chromStart'], errors='coerce')
        df['chromEnd'] = pd.to_numeric(df['chromEnd'], errors='coerce')
        
        # Drop any rows that failed conversion (bad data)
        df.dropna(subset=['copyNum', 'score', 'period', 'chromStart', 'chromEnd'], inplace=True)
        # --------------------------------------------------------

        # Filter: Keep only primary chromosomes
        df = df[~df['chrom'].str.contains('_')]
        
        print(f"Found {len(df)} repeat entries to process.")

        # Check if table is already populated
        existing_count = db.query(SimpleRepeat).count()
        if existing_count > 0:
            print(f"Table already has {existing_count} rows. Skipping load to avoid duplicates.")
            return

        print("Transforming data for database...")
        df = df.rename(columns={
            "chrom": "chromosome_name",
            "chromStart": "start_pos",
            "chromEnd": "end_pos",
            "period": "unit_size",
            "copyNum": "copy_num"
        })

        print("Bulk inserting into database (this might take a minute)...")
        data_to_insert = df.to_dict(orient='records')
        
        db.bulk_insert_mappings(SimpleRepeat, data_to_insert)
        db.commit()
        
        print("Successfully stored simple repeats!")

    except FileNotFoundError:
        print(f"ERROR: Could not find {REPEAT_FILE_PATH}. Did you download it?")
    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()
        print("Database session closed.")

if __name__ == "__main__":
    parse_and_store_repeats()