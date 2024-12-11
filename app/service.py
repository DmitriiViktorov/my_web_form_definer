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
    matches_template_names = []

    query_condition = [{key: {"$exists": True}} for key in data.keys()]
    query_filter = {"$or": query_condition}
    potential_templates = await forms_collection.find(query_filter).to_list(None)
    for template in potential_templates:
        template.pop("_id", None)
        print(template)
        if all(
            key in data and data[key] == field_type
            for key, field_type in template.items()
            if key != "name"
        ):
            matches_template_names.append(template["name"])

    return matches_template_names if matches_template_names else data