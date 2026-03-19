FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

ENV PYTHONPATH=/code
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python ingestion/ingest.py

CMD ["python", "bot/telegram_bot.py"]