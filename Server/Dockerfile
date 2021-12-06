FROM python:3.9-slim

Run pip install Flask gunicorn flask_restful flask_cors

COPY src/ /app

WORKDIR /app

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
