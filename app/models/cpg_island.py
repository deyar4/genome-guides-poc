from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class CpgIsland(Base):
    __tablename__ = "cpg_islands"

    id = Column(Integer, primary_key=True, index=True)
    chromosome_id = Column(Integer, ForeignKey("chromosomes.id"), nullable=False)
    start_pos = Column(Integer, index=True, nullable=False)
    end_pos = Column(Integer, index=True, nullable=False)
    name = Column(String, nullable=True) # Usually something like 'cpgIslandExt'
    
    # Statistics from UCSC format
    length = Column(Integer)
    cpg_num = Column(Integer)
    gc_num = Column(Integer)
    per_gc = Column(Integer) # Percentage GC
    per_cpg = Column(Integer) # Percentage CpG

    chromosome = relationship("Chromosome")
