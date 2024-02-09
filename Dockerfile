# Use an official Python runtime as a parent image
FROM python:latest

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /user-managment

# Copy the current directory contents into the container at /code
COPY . /user-managment/

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry using pip
RUN pip install poetry

# Install project dependencies
RUN poetry install

# Expose the port that the app runs on
EXPOSE 8000

# Run alembic migrations
RUN poetry run alembic upgrade head

# Command to run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
