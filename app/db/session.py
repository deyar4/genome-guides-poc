"""
    Database session management for SQLAlchemy.

    This module provides functions to get and manage the SQLAlchemy engine and
    session objects, ensuring lazy initialization and proper connection handling.
    It's designed to be the canonical source for database interaction setup.
    """
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..config import get_settings
from .base_class import Base # Import Base from its own file

# Use a dictionary to store engine and SessionLocal to avoid recreating them unnecessarily
_SessionLocal = None
_engine = None

def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        print(f"DEBUG: get_engine() creating engine with URL: {settings.SQLALCHEMY_DATABASE_URL}") # Debug print
        _engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
    return _engine

def get_session_local():
    global _SessionLocal
    engine = get_engine()
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return _SessionLocal

def get_db():
    """
    FastAPI dependency that yields a new SQLAlchemy session.
    Ensures the session is closed after the request is finished.
    """
    SessionLocal = get_session_local()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def reset_db_connection():
    """Resets the global engine and SessionLocal instances."""
    global _engine, _SessionLocal
    _engine = None
    _SessionLocal = None