FROM python:3.13-slim-bookworm

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc libc-dev pipx && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    groupadd -r app && useradd --no-log-init -r -g app -m app

WORKDIR /app
USER app
ENV PATH="/home/app/.local/bin:${PATH}"

COPY poetry.lock pyproject.toml ./
COPY app/ ./app/
RUN pipx install poetry && \
    poetry install --without dev -E pgsql

EXPOSE 8000

ENTRYPOINT [ "poetry" ]
CMD [ "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
