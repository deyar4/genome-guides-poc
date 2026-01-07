from pydantic import BaseModel
from typing import List, Optional

class SSR(BaseModel):
    chromosome_name: str
    motif: str
    count: int
    length: int
    start_position: int
    end_position: int

class SSRSummary(BaseModel):
    total_ssrs: int
    # Potentially add more summary statistics later, e.g.,
    # motifs_found: List[str]
    # average_length: float

class SSRResponse(BaseModel):
    # This schema will be used for the API response which will return a list of SSRs
    ssrs: List[SSR]
    # summary: SSRSummary # Could add a summary if desired

# Or, if we just want to return the raw list directly from the upserted statistic,
# the Statistic schema we already have (Dict[str, Any]) would suffice for the general case.
# However, defining a specific schema like SSRResponse is good for type-checking and API documentation.