import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_get_patient():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/patients/123456789")
        assert response.status_code == 200
        data = response.json()
        assert "ssn" in data