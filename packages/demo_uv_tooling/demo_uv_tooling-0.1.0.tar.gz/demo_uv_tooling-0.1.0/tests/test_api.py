import pytest
from httpx import ASGITransport
from httpx import AsyncClient

from src.main import app

@pytest.mark.anyio
async def test_request_completion():
    # Arrange
    prompt = "Hello, World!"

    # Act
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/completions/",
            json={
                "prompt": prompt,
            }
        )

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert data["prompt"] == prompt
        assert "id" in data

@pytest.mark.anyio
async def test_list_completions():
    # Act
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/completions/")

        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
