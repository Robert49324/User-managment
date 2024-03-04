#!/bin/bash
poetry run alembic upgrade head
poetry run pytest
poetry run python src/main.py 
