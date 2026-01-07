from pydantic import BaseModel, ConfigDict
from typing import List

class TelomereBase(BaseModel):
    """Base Pydantic schema for Telomere data, containing common fields."""
    chromosome_name: str
    start_position: int
    end_position: int
    length: int

class TelomereCreate(TelomereBase):
    """Pydantic schema for creating a new Telomere record."""
    pass

class Telomere(TelomereBase):
    """Pydantic schema for Telomere data as stored in the database, including its ID."""
    id: int

    model_config = ConfigDict(from_attributes=True)

class TelomereSequenceResponse(TelomereBase):
    """Pydantic schema for a Telomere response that includes the actual sequence."""
    sequence: str

class TelomeresResponse(BaseModel):
    """Pydantic schema for a list of Telomere sequence responses."""
    telomeres: List[TelomereSequenceResponse]