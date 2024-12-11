import pytest
from unittest.mock import AsyncMock, patch

from app.service import clean_user_data, find_template


@pytest.mark.asyncio
async def test_clean_user_data():
    user_data = {
        "birth_date": "01.01.2000",
        "phone_number": "+7 123 456 78 90",
        "email": "user@example.com",
        "name": "John Doe"
    }
    expected = {
        "birth_date": "date",
        "phone_number": "phone",
        "email": "email",
        "name": "text"
    }
    result = await clean_user_data(user_data)
    assert result == expected


@pytest.mark.asyncio
@patch("app.database.forms_collection.find")
async def test_find_template_with_match(mock_find):
    mock_find.return_value.to_list = AsyncMock(return_value=[
        {"name": "template1", "field1": "date", "field2": "email"},
        {"name": "template2", "field1": "phone", "field2": "text"},
    ])
    user_data = {"field1": "date", "field2": "email"}
    result = await find_template(user_data)
    assert result == ["template1"]

@pytest.mark.asyncio
@patch("app.database.forms_collection.find")
async def test_find_template_no_match(mock_find):
    mock_find.return_value.to_list = AsyncMock(return_value=[
        {"name": "template1", "field1": "date", "field2": "email"},
        {"name": "template2", "field1": "phone", "field2": "text"},
    ])
    user_data = {"field1": "text", "field3": "phone"}
    result = await find_template(user_data)
    assert result == user_data


@pytest.mark.asyncio
@patch("app.database.forms_collection.find")
async def test_find_template_multi_match(mock_find):
    mock_find.return_value.to_list = AsyncMock(return_value=[
        {"name": "template1", "field1": "date", "field2": "email"},
        {"name": "template2", "field1": "date", "field3": "text"},
    ])
    user_data = {"field1": "date", "field2": "email", "field3": "text"}
    result = await find_template(user_data)
    assert result == ["template1", "template2"]

@pytest.mark.asyncio
@patch("app.database.forms_collection.find")
async def test_find_template_almost_match(mock_find):
    mock_find.return_value.to_list = AsyncMock(return_value=[
        {"name": "template1", "field1": "date", "field2": "email"},
        {"name": "template2", "field1": "date", "field3": "text"},
    ])
    user_data = {"field1": "date", "field_2": "email",}
    result = await find_template(user_data)
    assert result == user_data

