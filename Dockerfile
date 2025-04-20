FROM python:3.11-slim-buster

EXPOSE 8000
WORKDIR /app

RUN apt-get update && \
  apt-get install -y --no-install-recommends libpq-dev gcc libc-dev && \
  rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

COPY poetry.lock pyproject.toml ./
RUN pip install poetry==1.1.4 && \
  poetry install --no-dev -E pgsql

COPY app/ ./app/

ENTRYPOINT [ "poetry" ]
CMD [ "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]
