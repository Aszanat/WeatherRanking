from typing import Union
from fastapi import FastAPI, HTTPException
from openmeteo import connect_to_openmeteo
from datetime import date, timedelta

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.get("/api/v1/cities-scores")
def get_cities_scores(start_date: Union[str, None] = None, end_date: Union[str, None] = None):
    if not start_date:
        start_date = date.today() - timedelta(days=1)
    else:
        start_date = date.fromisoformat(start_date)
    if not end_date:
        end_date = date.today() - timedelta(days=1)
        if end_date - start_date < timedelta(days=0):
            end_date = start_date
    else:
        end_date = date.fromisoformat(end_date)
    if end_date - start_date < timedelta(days=0):
        raise HTTPException(status_code=400, detail="end_date is earlier than start_date")

    return connect_to_openmeteo(start_date, end_date)