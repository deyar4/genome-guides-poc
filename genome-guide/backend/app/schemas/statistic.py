from pydantic import BaseModel, ConfigDict
from typing import Dict, Any

class Statistic(BaseModel):
    stat_name: str
    # Change the type from 'Json' to 'Dict[str, Any]' or just 'dict'
    stat_value: Dict[str, Any]
    model_config = ConfigDict(from_attributes=True)