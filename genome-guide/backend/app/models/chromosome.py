from sqlalchemy import Column, Integer, String, Text
from ..db.session import Base

class Chromosome(Base):
    __tablename__ = "chromosomes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    length = Column(Integer, nullable=False)
    # Storing the full sequence make the DB big. But it's good for adding modularity and our database can still handle it.
    sequence = Column(Text)