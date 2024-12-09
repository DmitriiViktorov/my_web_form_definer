from fastapi import FastAPI


app = FastAPI()


@app.post("/get_form")
async def get_form():
    pass