from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Exon(Base):
    __tablename__ = "exons"

    id = Column(Integer, primary_key=True, index=True)
    # Link to the Gene table using the gene_id string (e.g., ENSG000001...)
    # Note: It's often safer/faster to link via the internal Integer ID, 
    # but GTF provides the string ID. Let's use the string ID for the Foreign Key 
    # but we need to ensure the parent Gene table has it indexed (which it does).
    gene_id = Column(String, ForeignKey("genes.gene_id"), index=True, nullable=False)
    
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    
    # We might want the exon number (e.g., 1, 2, 3)
    exon_number = Column(Integer)