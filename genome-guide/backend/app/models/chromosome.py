from sqlalchemy import Column, Integer, String, Text
from ..db.session import Base

class Chromosome(Base):
    __tablename__ = "chromosomes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    length = Column(Integer, nullable=False)
    # Storing the full sequence is possible but can make the DB huge.
    # For now, let's omit it and focus on metadata. We can add it later if needed.
    # sequence = Column(Text)