FROM python:3.9-slim

Run pip install -r requirements.txt
Run pip install gunicorn

COPY src/ src/

WORKDIR /src

ENV PYTHONPATH /

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
