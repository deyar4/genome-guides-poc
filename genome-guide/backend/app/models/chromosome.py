from sqlalchemy import Column, Integer, String, Text
from ..db.base_class import Base

class Chromosome(Base):
    __tablename__ = "chromosomes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    length = Column(Integer, nullable=False)
    sequence = Column(Text, nullable=True) # Added sequence column