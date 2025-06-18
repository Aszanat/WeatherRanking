FROM python:3.13-slim

WORKDIR /usr/src/app

COPY . .

# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r requirements.txt

EXPOSE 7890

ENTRYPOINT ["uvicorn", "app:app", "--reload", "--port", "7890", "--host", "0.0.0.0"]