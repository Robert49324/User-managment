#!/bin/bash
poetry run alembic upgrade head
poetry run pytest --cov
poetry run python src/main.py 
