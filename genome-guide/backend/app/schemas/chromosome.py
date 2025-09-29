from pydantic import BaseModel

class ChromosomeBase(BaseModel):
    name: str
    length: int

class ChromosomeCreate(ChromosomeBase):
    pass

class Chromosome(ChromosomeBase):
    id: int

    class Config:
        # This is the line to change
        from_attributes = True