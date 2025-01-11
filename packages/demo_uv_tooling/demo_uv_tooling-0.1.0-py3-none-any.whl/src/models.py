from pydantic import BaseModel
from pydantic import Field

class CompletionRequest(BaseModel):
    """Schema for creating a new completion."""
    prompt: str = Field(..., min_length=1, max_length=200)

class CompletionResponse(CompletionRequest):
    """Schema for a completion with ID."""
    response: str = Field(..., min_length=1, max_length=500)
    id: int = Field(..., gt=0)
