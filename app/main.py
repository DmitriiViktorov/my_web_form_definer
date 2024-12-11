from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from .database import initialize_database, forms_collection
from .service import find_template, clean_user_data, get_all_templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database(forms_collection)
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/get_form")
async def get_form(request: Request):
    """
    Эндпоинт для поиска формы, соответствующей полям и типам данных в этих полях.
    Эндпоинт получает данные от пользователя в виде query params из запроса,
    проводит валидацию и "типизацию" данных пользователя, после чего отправляет очищенные данные
    для поиска совпадений с шаблонами в базе данных
    :param request: Запрос пользователя
    :return: результат поиска совпадений с шаблонами в базе данных
    """
    user_form_data = dict(request.query_params)
    if not user_form_data:
        return JSONResponse(status_code=404, content={
            "error": {
                "message": "There are no parameters in the request."
            }
        })

    empty_fields = [key for key, value in user_form_data.items() if not value]
    if empty_fields:
        return JSONResponse(status_code=400, content={
            "error": {
                "message": f"Empty fields found: {', '.join(empty_fields)}"
            }
        })
    cleaned_user_data = await clean_user_data(user_form_data)

    result = await find_template(cleaned_user_data)
    return result

@app.get("/get_all_templates")
async def get_templates(request: Request):
    """Запрос для быстрого просмотра всех имеющихся шаблонов в базе данных"""
    result = await get_all_templates()
    for template in result:
        template.pop("_id", None)
    return result
