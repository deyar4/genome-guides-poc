from pydantic import BaseModel

# We'll define a simple schema for the nested chromosome data
class ChromosomeInGeneResponse(BaseModel):
    name: str
    length: int

    class Config:
        from_attributes = True


class GeneBase(BaseModel):
    gene_id: str
    gene_name: str | None = None
    start_pos: int
    end_pos: int
    strand: str

class GeneCreate(GeneBase):
    pass

# This is the main schema for API responses
class Gene(GeneBase):
    id: int
    # Instead of 'chromosome_id', we now expect a 'chromosome' object
    # that matches the shape of our new ChromosomeInGeneResponse schema
    chromosome: ChromosomeInGeneResponse

    class Config:
        from_attributes = True