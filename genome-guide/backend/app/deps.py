from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from .database import SessionLocal

@contextmanager
def session_scope() -> Iterator:
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

# FastAPI dependency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()