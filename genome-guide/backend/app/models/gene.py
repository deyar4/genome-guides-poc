from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Gene(Base):
    __tablename__ = "genes"

    id = Column(Integer, primary_key=True, index=True)
    gene_id = Column(String, unique=True, index=True, nullable=False)
    gene_name = Column(String, index=True)
    gene_type = Column(String, index=True) 
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    strand = Column(String(1), nullable=False)

    chromosome_id = Column(Integer, ForeignKey("chromosomes.id"), nullable=False)
    chromosome = relationship("Chromosome")