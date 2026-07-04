FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 \
    MKL_NUM_THREADS=1 \
    NUMEXPR_NUM_THREADS=1

WORKDIR /app

RUN addgroup --system app && adduser --system --ingroup app app

COPY pyproject.toml ./
COPY app ./app
COPY migrations ./migrations
COPY seeds ./seeds
COPY artifacts ./artifacts
COPY alembic.ini wsgi.py ./

RUN python -m pip install --upgrade pip==26.1.2 \
    && python -m pip install . \
    && chown -R app:app /app \
    && chmod -R a-w /app/artifacts

USER app
EXPOSE 8000

CMD ["gunicorn", "--bind=0.0.0.0:8000", "--workers=2", "--timeout=30", "--graceful-timeout=30", "wsgi:app"]
