from pydantic import BaseModel, ConfigDict

class ChromosomeBase(BaseModel):
    name: str
    length: int

class ChromosomeCreate(ChromosomeBase):
    pass

class Chromosome(ChromosomeBase):
    id: int
    model_config = ConfigDict(from_attributes=True)