import sys, os
from sqlalchemy import text
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.db.session import SessionLocal

def drop_genes_table():
    db = SessionLocal()
    print("Dropping 'genes' and 'exons' tables to force a schema update...")
    try:
        # We drop exons first because it depends on genes
        db.execute(text("DROP TABLE IF EXISTS exons"))
        db.execute(text("DROP TABLE IF EXISTS genes"))
        db.commit()
        print("Tables dropped. You can now run parse_gtf.py.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    drop_genes_table()