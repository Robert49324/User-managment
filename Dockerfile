FROM python:3.12.1

RUN pip install poetry

RUN pip install alembic

WORKDIR /app

COPY . .

RUN poetry install

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
