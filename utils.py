from datetime import date
from fastapi import HTTPException


def parse_date(str_date: date, date_name: str):
    try:
        return date.fromisoformat(str_date)
    except ValueError:
        raise HTTPException(status_code=400, detail=f"{date_name} should be an actual date!")