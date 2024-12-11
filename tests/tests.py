import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_index(client):
    user_data = {"username": "Dmitrii", "email": "viktorovokrl@gmail.com"}
    response = client.post("/get_form", params=user_data)
    assert response.status_code == 200
    assert response.json() == ["User authentication"]