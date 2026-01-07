from sqlalchemy import Column, Integer, String, Text, JSON
from ..db.base_class import Base

class GenomeStatistic(Base):
    __tablename__ = "genome_stats"

    id = Column(Integer, primary_key=True, index=True)
    # The name of the statistic, e.g., "nuclear_base_composition"
    stat_name = Column(String, unique=True, index=True, nullable=False)
    # The value of the statistic, stored as a JSON object
    stat_value = Column(JSON, nullable=False)