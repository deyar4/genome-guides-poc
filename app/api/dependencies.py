from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from ..db.session import get_session_local

@contextmanager
def session_scope() -> Iterator:
    SessionLocal = get_session_local()
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
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()