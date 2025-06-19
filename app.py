from typing import Union
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from openmeteo import connect_to_openmeteo
from datetime import date, timedelta

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
def gui(request: Request, response_class=HTMLResponse):
    yesterday = date.today() - timedelta(days=1)
    start_date = request.query_params.get("start_date")
    end_date = request.query_params.get("end_date")
    if not start_date:
        start_date = yesterday
    if not end_date:
        end_date = yesterday
    cities_scores = []

    if request.query_params:
        cities_scores = get_cities_scores(start_date=start_date, end_date=end_date)

    context = {"request": request, \
        "start_date": start_date, \
        "end_date": end_date, \
        "cities_scores": cities_scores}

    return templates.TemplateResponse("gui.html", context)

@app.get("/api/v1/cities-scores")
def get_cities_scores(start_date: Union[str, date, None] = None, end_date: Union[str, date, None] = None):
    if start_date and end_date:
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)
        if end_date - start_date < timedelta(days=0):
            raise HTTPException(status_code=400, detail="end_date is earlier than start_date")
    elif start_date:
        if isinstance(start_date, str):
            start_date = date.fromisoformat(start_date)
        end_date = start_date
    elif end_date:
        if isinstance(end_date, str):
            end_date = date.fromisoformat(end_date)
        start_date = end_date
    else:
        end_date = date.today() - timedelta(days=1)
        start_date = end_date
    
    return connect_to_openmeteo(start_date, end_date)