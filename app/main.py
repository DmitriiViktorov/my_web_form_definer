from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from .database import initialize_database
from .service import find_template, clean_user_data, get_all_templates

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_database()
    yield

app = FastAPI(lifespan=lifespan)


@app.post("/get_form")
async def get_form(request: Request):
    user_form_data = dict(request.query_params)
    cleaned_user_data = await clean_user_data(user_form_data)

    result = await find_template(cleaned_user_data)
    return result

@app.get("/get_all_templates")
async def get_templates(request: Request):
    result = await get_all_templates()
    for template in result:
        template.pop("_id", None)
    return result
