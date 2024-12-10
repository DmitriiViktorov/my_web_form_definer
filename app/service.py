from .database import forms_collection
from .validator import validate_field

async def get_all_templates():
    templates = await forms_collection.find().to_list(length=1000)
    return templates

async def clean_user_data(user_data: dict) -> dict:
    cleaned_data = {}
    for key, value in user_data.items():
        cleaned_data[key] = validate_field(value)
    return cleaned_data

async def find_template(data: dict):
    result = await forms_collection.find_one(data, {"_id": 0, "name": 1})
    return result if result else data