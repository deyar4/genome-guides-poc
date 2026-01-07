from pydantic import BaseModel, ConfigDict
from typing import List, Optional, Any

class VariantBase(BaseModel):
    rsid: str
    chromosome: str
    position: int
    reference: str
    alternate: str
    gene_symbol: str
    clinical_significance: str = ""

class VariantCreate(VariantBase):
    pass

class VariantOut(VariantBase):
    id: int
    model_config = ConfigDict(from_attributes=True)