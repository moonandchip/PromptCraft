FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir poetry==2.3.2

COPY pyproject.toml poetry.lock ./
RUN poetry install --only main --no-root --no-interaction --no-ansi

COPY app ./app

EXPOSE 8000

CMD ["sh", "-c", "poetry run alembic upgrade head && exec poetry run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2"]
