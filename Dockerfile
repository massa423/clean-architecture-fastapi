FROM python:3.11-slim-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc-dev && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    groupadd -r app && useradd --no-log-init -r -g app -m app

WORKDIR /app
USER app
ENV PATH="/home/app/.local/bin:${PATH}"

COPY uv.lock pyproject.toml ./
COPY app/ ./app/
RUN uv sync --no-dev --extra pgsql --frozen

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
