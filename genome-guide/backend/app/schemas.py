from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

# -------------------- Gene --------------------
class Gene(BaseModel):
    id: str
    name: str
    description: str | None = None
    chromosome: str
    start: int
    end: int

class GeneBase(BaseModel):
    symbol: str
    name: str
    description: str = ""
    chromosome: str
    start_position: int
    end_position: int
    strand: str
    gene_type: str = "protein_coding"
    species: str = "Homo sapiens"

class GeneCreate(GeneBase):
    pass

class GeneOut(BaseModel):
    id: int
    symbol: str
    name: str
    chromosome: str
    start: int = Field(alias="start_position")
    end: int = Field(alias="end_position")
    strand: str
    gene_type: str
    species: str
    description: str = ""

    model_config = ConfigDict(from_attributes=True)


# -------------------- Variant --------------------
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

# -------------------- Misc --------------------
class GenomeRegion(BaseModel):
    chromosome: str
    start: int
    end: int

class GeneSearchResponse(BaseModel):
    results: List[GeneOut]