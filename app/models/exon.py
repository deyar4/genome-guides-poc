from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class Exon(Base):
    __tablename__ = "exons"

    id = Column(Integer, primary_key=True, index=True)
    gene_id = Column(Integer, ForeignKey("genes.id"), nullable=False)
    start_pos = Column(Integer, index=True, nullable=False)
    end_pos = Column(Integer, index=True, nullable=False)
    exon_number = Column(Integer)

    gene = relationship("Gene", backref="exons")
