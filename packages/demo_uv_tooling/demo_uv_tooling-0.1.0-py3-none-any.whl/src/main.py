from fastapi import FastAPI
from src.models import CompletionRequest, CompletionResponse
from src.text_generation import generate_text

app: FastAPI = FastAPI(
    title="UV Demo API",
)

# In-memory storage for demo
completions: list[CompletionResponse] = []

@app.post("/completions/", response_model=CompletionResponse)
async def create_completion(
    completion_request: CompletionRequest
) -> CompletionResponse:
    """Create a new completion."""
    print(completion_request)
    completion_response = CompletionResponse(
        id=len(completions) + 1,
        prompt=completion_request.prompt,
        response=generate_text(prompt=completion_request.prompt),
    )
    completions.append(completion_response)
    print(completion_response)
    return completion_response

@app.get("/completions/", response_model=list[CompletionResponse])
async def list_completions() -> list[CompletionResponse]:
    """List all completions."""
    return completions
