FROM python:3.12-slim

WORKDIR /app

COPY ./app /app

RUN pip install --no-cache-dir -r /app/requirements.txt

CMD ["python", "main.py"]