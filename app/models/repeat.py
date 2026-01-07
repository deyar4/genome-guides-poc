from sqlalchemy import Column, Integer, String, Text, Float
from ..db.session import Base

class SimpleRepeat(Base):
    __tablename__ = "simple_repeats"

    # standard integer ID
    id = Column(Integer, primary_key=True, index=True)
    
    # Location info
    chromosome_name = Column(String, index=True, nullable=False) # e.g. "chr1"
    start_pos = Column(Integer, nullable=False)
    end_pos = Column(Integer, nullable=False)
    
    # Repeat Statistics (from the UCSC file)
    unit_size = Column(Integer, index=True) # e.g. 3 for "CAG"
    period = Column(Integer)                # Similar to unit_size
    copy_num = Column(Float)                # How many times it repeats (e.g. 12.5)
    score = Column(Float)                   # Alignment score
    
    # The sequence itself
    sequence = Column(Text, nullable=False) # The repeating unit, e.g. "CAG"