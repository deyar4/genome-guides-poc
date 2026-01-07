from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class NonCodingRNA(Base):
    __tablename__ = "non_coding_rnas"

    id = Column(Integer, primary_key=True, index=True)
    chromosome_id = Column(Integer, ForeignKey("chromosomes.id"), nullable=False, index=True)
    start_pos = Column(Integer, index=True, nullable=False)
    end_pos = Column(Integer, index=True, nullable=False)
    strand = Column(String(1))
    rna_type = Column(String, index=True) # e.g. rRNA, tRNA, snRNA
    rna_class = Column(String, index=True) # repClass from rmsk
    rna_name = Column(String) # repName from rmsk

    chromosome = relationship("Chromosome")
