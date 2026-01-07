from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field

from . import gene as gene_schemas # Import the gene schema

# -------------------- Misc --------------------
class GenomeRegion(BaseModel):
    chromosome: str
    start: int
    end: int

class GeneSearchResponse(BaseModel):
    results: List[gene_schemas.Gene] # Correctly reference the Gene schema
