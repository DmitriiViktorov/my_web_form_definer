from fastapi import FastAPI, Request
from .service import find_template, clean_user_data
app = FastAPI()


@app.post("/get_form")
async def get_form(request: Request):
    user_form_data = dict(request.query_params)
    cleaned_user_data = await clean_user_data(user_form_data)

    result = await find_template(cleaned_user_data)
    return result
