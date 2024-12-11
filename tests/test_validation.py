import pytest
from app.validator import validate_field, validate_date

@pytest.mark.parametrize("date_input, expected", [
    ("12.03.2023", True),
    ("2023-03-12", True),
    ("31.02.2023", False),
    ("12-03-2023", False),
    ("March 12, 2023", False),
    ("12/03/2023", False),
])
def test_validate_date(date_input, expected):
    assert validate_date(date_input) == expected

@pytest.mark.parametrize("field_value, expected", [
    ("12.03.2023", "date"),
    ("2023-03-12", "date"),
    ("+7 911 123 45 67", "phone"),
    ("+7 911 123 4567", "text"),
    ("8 911 123 45 67", "text"),
    ("viktorovokrl@gmail.com", "email"),
    ("viktorovokrl@gmail", "text"),
    ("notanemail@", "text"),
    ("randomtext", "text"),
])
def test_validate_field(field_value, expected):
    assert validate_field(field_value) == expected
