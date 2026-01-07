from sqlalchemy import Column, Integer, String
from ..db.base_class import Base

class Centromere(Base):
    __tablename__ = "centromeres"

    id = Column(Integer, primary_key=True, index=True)
    chromosome_name = Column(String, index=True, nullable=False)
    start_position = Column(Integer, nullable=False)
    end_position = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
