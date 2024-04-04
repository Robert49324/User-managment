#!/bin/bash
poetry run alembic upgrade head
poetry run python src/main.py 
