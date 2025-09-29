from pydantic import BaseModel

class GeneBase(BaseModel):
    gene_id: str
    gene_name: str | None = None
    start_pos: int
    end_pos: int
    strand: str

class GeneCreate(GeneBase):
    pass

class Gene(GeneBase):
    id: int
    chromosome_id: int

    class Config:
        from_attributes = True