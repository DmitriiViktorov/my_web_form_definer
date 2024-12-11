import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def test_client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_data():
    return {
        "username": "Dmitrii",
        "email": "viktorovokrl@gmail.com"
    }
