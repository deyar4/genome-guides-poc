import json
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.statistic import GenomeStatistic

def get_db_session() -> Session:
    """Provides a database session."""
    return SessionLocal()

def upsert_statistic(db: Session, name: str, value: dict):
    """Updates a statistic if it exists, or creates it if it doesn't."""
    existing_stat = db.query(GenomeStatistic).filter(GenomeStatistic.stat_name == name).first()
    # Ensure data is JSON-serializable (converts Counter to dict)
    stat_value_json = json.loads(json.dumps(value))

    if existing_stat:
        existing_stat.stat_value = stat_value_json
        print(f"Updating statistic: {name}")
    else:
        new_stat = GenomeStatistic(stat_name=name, stat_value=stat_value_json)
        db.add(new_stat)
        print(f"Creating new statistic: {name}")

    db.commit()