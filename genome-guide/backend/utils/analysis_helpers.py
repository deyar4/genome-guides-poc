import json
from sqlalchemy.orm import Session
from app.db.session import get_session_local
from app.models.statistic import GenomeStatistic
from collections import Counter
import contextlib

@contextlib.contextmanager
def get_db_session():
    """
    Provides a database session as a context manager, ensuring the session is
    committed on success and rolled back on failure.
    """
    SessionLocal = get_session_local()
    db: Session = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

def _json_serializable(obj):
    if isinstance(obj, Counter):
        return {str(k): v for k, v in obj.items()}
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def upsert_statistic(db: Session, name: str, value: dict):
    existing_stat = db.query(GenomeStatistic).filter(GenomeStatistic.stat_name == name).first()
    stat_value_json = json.dumps(value, default=_json_serializable)
    
    if existing_stat:
        existing_stat.stat_value = json.loads(stat_value_json)
        print(f"Updating statistic: {name}")
    else:
        new_stat = GenomeStatistic(stat_name=name, stat_value=json.loads(stat_value_json))
        db.add(new_stat)
        print(f"Creating new statistic: {name}")
