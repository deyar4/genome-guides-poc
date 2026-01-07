from sqlalchemy import Column, Integer, String
from ..db.base_class import Base

class Telomere(Base):
    """
    SQLAlchemy ORM model for Telomere regions.
    Represents telomere locations within chromosomes in the database.
    """
    __tablename__ = "telomeres"

    id = Column(Integer, primary_key=True, index=True)
    chromosome_name = Column(String, index=True, nullable=False)
    start_position = Column(Integer, nullable=False)
    end_position = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)