"""
    Base class for SQLAlchemy declarative models.
    All ORM models in the application should inherit from this Base.
    """
from sqlalchemy.orm import declarative_base

Base = declarative_base()
"""
SQLAlchemy declarative base class. 
It serves as the foundation for defining ORM models.
"""