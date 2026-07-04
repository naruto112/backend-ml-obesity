FROM python:3.10.18-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml ./
COPY app ./app
COPY migrations ./migrations
COPY seeds ./seeds
COPY alembic.ini wsgi.py ./

RUN python -m pip install --upgrade pip==26.1.2 \
    && python -m pip install . \
    && chown -R app:app /app

USER app
EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "--timeout=30", "--graceful-timeout=30", "wsgi:app"]
