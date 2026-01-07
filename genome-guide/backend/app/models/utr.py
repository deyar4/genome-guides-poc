from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.base_class import Base

class Utr(Base):
    __tablename__ = "utrs"

    id = Column(Integer, primary_key=True, index=True)
    gene_id = Column(Integer, ForeignKey("genes.id"), nullable=False)
    start_pos = Column(Integer, index=True, nullable=False)
    end_pos = Column(Integer, index=True, nullable=False)
    utr_type = Column(String) # '5_prime_utr' or '3_prime_utr'

    gene = relationship("Gene", backref="utrs")
