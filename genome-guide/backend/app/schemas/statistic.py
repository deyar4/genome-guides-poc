from pydantic import BaseModel
from typing import Dict, Any

class Statistic(BaseModel):
    stat_name: str
    # Change the type from 'Json' to 'Dict[str, Any]' or just 'dict'
    stat_value: Dict[str, Any]

    class Config:
        from_attributes = True