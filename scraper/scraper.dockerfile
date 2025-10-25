FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY core/ ./core/
COPY scraper/ ./scraper/

CMD python -m scraper.main
