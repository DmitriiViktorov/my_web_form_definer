import pytest
from httpx import AsyncClient
import pytest
from httpx import ASGITransport, AsyncClient
from app.main import app



@pytest.mark.asyncio
async def test_correct_user_data(test_client):
    user_data = {
        "username": "Dmitrii",
        "email": "viktorovokrl@gmail.com"
    }
    response = test_client.post("/get_form", params=user_data)
    assert response.status_code == 200
    assert response.json() == ["User authentication"]

@pytest.mark.asyncio
async def test_unmatched_user_data(test_client):
    user_data = {
        "e-mail": "viktorovokrl@gmail.com",
        "address": "London SW1A 0AA, England",
        "lat-lon": (51.5007, 0.1245)
    }
    response = test_client.post("/get_form", params=user_data)
    assert response.status_code == 200
    expected_data = {
        "e-mail": "email",
        "address": "text",
        "lat-lon": "text",
    }
    assert response.json() == expected_data

@pytest.mark.asyncio
async def test_incorrect_user_data_types(test_client):
    user_data = {
        "username": "11.03.2022",
        "password": "+7 953 333 22 11",
    }
    response = test_client.post("/get_form", params=user_data)
    assert response.status_code == 200
    expected_data = {
        "username": "date",
        "password": "phone",
    }
    assert response.json() == expected_data

@pytest.mark.asyncio
async def test_multiply_templates(test_client, test_data):
    expanded_user_data = test_data.copy()
    expanded_user_data["password"] = "{my_secret_password}"
    response = test_client.post("/get_form", params=expanded_user_data)
    assert response.status_code == 200
    assert response.json() == [
        "User authentication",
        "User login"
    ]

@pytest.mark.asyncio
async def test_empty_params(test_client):
    response = test_client.post("/get_form")
    assert response.status_code == 404
    assert response.json() == {"error": {"message": "There are no parameters in the request."}}

@pytest.mark.asyncio
async def test_incorrect_method(test_client, test_data):
    response = test_client.get("/get_form", params=test_data)
    assert response.status_code == 405
    assert response.json()['detail'] == 'Method Not Allowed'