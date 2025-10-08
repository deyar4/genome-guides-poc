from pydantic import BaseModel, Json

class Statistic(BaseModel):
    stat_name: str
    stat_value: Json

    class Config:
        from_attributes = True