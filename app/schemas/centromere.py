from pydantic import BaseModel, ConfigDict

class CentromereBase(BaseModel):
    chromosome_name: str
    start_position: int
    end_position: int
    length: int

class CentromereCreate(CentromereBase):
    pass

class Centromere(CentromereBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CentromereSequenceResponse(BaseModel):
    chromosome_name: str
    start_position: int
    end_position: int
    length: int
    sequence: str