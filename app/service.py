from typing import Any

from .database import forms_collection
from .validator import validate_field

async def get_all_templates() -> list[dict]:
    """Функция возвращает все имеющиеся шаблоны из базы данных"""
    templates = await forms_collection.find().to_list(length=1000)
    return templates

async def clean_user_data(user_data: dict[str, Any]) -> dict[str, str]:
    """
    Проводит валидацию и типизацию данных пользователя.
    Получает данные в виде словаря, каждому значению в словаре подбирается соответствующий тип.
    Возвращает обновленный "типизированный" словарь.
    :param user_data: Данные пользователя.
    :return: Типизированные данные пользователя
    """
    cleaned_data = {}
    for key, value in user_data.items():
        cleaned_data[key] = validate_field(value)
    return cleaned_data

async def find_template(data: dict) -> list[str]:
    """
    Производит поиск "подходящего" шаблона в базе данных.
    Получает типизированные данные пользователя.
    По всем имеющимся ключам в данных пользователя формируется фильтр для запроса в БД.
    Проводится выборка всех шаблонов, в которых есть хотя бы одно поле из данных пользователя.
    Для полученного списка шаблонов проводится поиск тех шаблонов, в которых каждое поле шаблона
    присутствует в данных пользователя и тип данных для каждого поля совпадает.
    В случае успеха возвращает список подходящих шаблонов.
    В другом случае возвращает типизированные данные пользователя
    :param data: Данные пользователя
    :return: Список названий подходящих шаблонов или типизированные данные пользователя.
    """
    matches_template_names = []

    query_condition = [{key: {"$exists": True}} for key in data.keys()]
    query_filter = {"$or": query_condition}
    potential_templates = await forms_collection.find(query_filter).to_list(None)
    for template in potential_templates:
        template.pop("_id", None)
        if all(
            key in data and data[key] == field_type
            for key, field_type in template.items()
            if key != "name"
        ):
            matches_template_names.append(template["name"])

    return matches_template_names if matches_template_names else data