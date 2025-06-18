from typing import Union
from fastapi import FastAPI
from openmeteo import connect_to_openmeteo

app = FastAPI()

@app.get("/")
def read_root():
    connect_to_openmeteo()
    return {"Hello": "World!"}