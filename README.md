## Overview

A simple user CRUD API built with FastAPI, implemented following Clean Architecture principles.

[日本語版はこちら](docs/README.ja.md)

## Local Development Setup

### Prerequisites

- uv >= 0.5
- Python >= 3.11
- sqlite3

### Install Dependencies

```
$ uv sync
```

### Database Initialization

#### Initialize the DB

```
$ export PYTHONPATH="$(pwd):$PYTHONPATH"
$ python app/init_db.py
```

#### Verify the DB

```
$ sqlite3 sample_db.sqlite3
```

Check tables:

```
> .tables
users
```

Check records:

```
> select * from users;
1|squid|5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8|squid@example.com|2021-01-11 22:35:50.033582|2021-01-11 22:35:50.033582
2|octopus|5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8|octopus@example.com|2021-01-11 22:35:50.034306|2021-01-11 22:35:50.034306
```

### Start the Application

```
$ uv run task dev
```

Visit http://127.0.0.1:8000/docs.

## Development Tasks

Available tasks via [taskipy](https://github.com/taskipy/taskipy):

| Task | Command | Description |
|------|---------|-------------|
| `uv run task dev` | `uvicorn app.main:app --reload` | Start dev server |
| `uv run task lint` | `flake8 .` | Run linter |
| `uv run task format` | `black .` | Format code |
| `uv run task typecheck` | `mypy .` | Run type checker |

## Docker Setup

### Prerequisites

- postgresql (Mac)
  - `brew install postgresql`
- Docker

  - [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
  - [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)
  - [Server](https://docs.docker.com/engine/install/)

- docker-compose
  - Included with Docker Desktop. For server installs, [install separately](https://docs.docker.com/compose/install/).

### Create Containers

#### Configure Environment Variables

Copy and edit the sample env files:

```
$ cp -p .env-app.sample .env-app
$ cp -p .env-postgresql.sample .env-postgresql
```

#### Start Containers

```
$ docker-compose up -d
$ docker-compose ps                                                                    master ◼
  Name                Command               State            Ports
---------------------------------------------------------------------------
api        uv run uvicorn app.mai ...      Up      0.0.0.0:8000->8000/tcp
postgres   docker-entrypoint.sh postgres    Up      5432/tcp
```

### Initialize the Database

```
$ docker exec -it -e PYTHONPATH="/app:$PYTHONPATH" api uv run python app/init_db.py
```

#### Verify the DB

```
$ docker-compose exec db psql -U postgres testdb
```

Check tables:

```
# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)
```

Check records:

```
# select * from users;
 id |  name   |                             password                             |        email        |         created_at         |         updated_at
----+---------+------------------------------------------------------------------+---------------------+----------------------------+----------------------------
  1 | squid   | 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | squid@example.com   | 2020-12-29 21:03:09.169173 | 2020-12-29 21:03:09.169173
  2 | octopus | 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | octopus@example.com | 2020-12-29 21:03:09.173484 | 2020-12-29 21:03:09.173484
(2 rows)
```

Visit http://127.0.0.1:8000/docs.

## Running Tests

```
$ pytest
```

## Project Structure

```
app
├── api                - API layer
│   └── v1             - API v1
│       └── endpoints  - Endpoint handlers
├── core               - Config, logger, etc.
├── domains            - Enterprise Business Rules
├── exceptions         - Custom exceptions
├── injector           - Dependency injection
├── interfaces         - Interface Adapters
│   └── gateways       - External resource access (DB, etc.)
└── usecases           - Application Business Rules
    └── users          - User operations
```

## References

- [FastAPI](https://fastapi.tiangolo.com/)
  - [tiangolo/fastapi (Github)](https://github.com/tiangolo/fastapi)
  - [tiangolo/full-stack-fastapi-postgresql (Github)](https://github.com/tiangolo/full-stack-fastapi-postgresql)
  - [nsidnev/fastapi-realworld-example-app (Github)](https://github.com/nsidnev/fastapi-realworld-example-app)
- [Starlette](https://www.starlette.io/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
