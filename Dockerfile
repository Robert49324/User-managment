FROM python:3.12.1-slim

ENV PYTHONPATH "/app/src"
ENV PYTHONPATH "/app"

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

RUN pip install poetry==1.7.1 && poetry install && chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
