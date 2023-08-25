FROM python:3.11

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY /app /app

ENV FILE .env

EXPOSE 8000 


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]