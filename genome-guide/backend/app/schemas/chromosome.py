from pydantic import BaseModel

class ChromosomeBase(BaseModel):
    name: str
    length: int

class ChromosomeCreate(ChromosomeBase):
    pass

class Chromosome(ChromosomeBase):
    id: int

    class Config:
        from_attributes = True