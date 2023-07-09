## 概要

クリーンアーキテクチャ(Clean Architecture)で実装した FastAPI ベースのシンプルな
ユーザ操作(CRUD)API。

## ローカル開発環境構築

### 前提

- Python 3.11
- sqlite3

### アプリケーション環境構築

Python ライブラリのインストール。

```
$ pip install poetry
```

### データベース初期化

#### DB を初期化

```
$ export PYTHONPATH="$(pwd):$PYTHONPATH"
$ python app/init_db.py
```

#### 作成された DB の確認

```
$ sqlite3 sample_db.sqlite3
```

テーブルの確認。

```
> .tables
users
```

レコードの確認。

```
> select * from users;
1|squid|5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8|squid@example.com|2021-01-11 22:35:50.033582|2021-01-11 22:35:50.033582
2|octopus|5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8|octopus@example.com|2021-01-11 22:35:50.034306|2021-01-11 22:35:50.034306
```

### アプリケーション起動

```
$ uvicorn app.main:app --reload
```

http://127.0.0.1:8000/docs へアクセス。

## Docker 環境構築

### 前提

- postgresql (Mac)
  - `brew install postgresql`
- Docker

  - [Docker Desktop for Mac](https://docs.docker.com/docker-for-mac/install/)
  - [Docker Desktop for Windows](https://docs.docker.com/docker-for-windows/install/)
  - [Server](https://docs.docker.com/engine/install/)

- docker-compose
  - Desktop 版であれば docker-compose が同梱されているが、Server 版の場合は別途[インストール](https://docs.docker.com/compose/install/)が必要。

### コンテナ作成

#### 環境変数の設定

`.env-app.sample`、`.env-postgresql.sample`をリネームし、適宜編集する。

```
$ cp -p .env-app.sample .env-app
$ cp -p .env-postgresql.sample .env-postgresql
```

#### コンテナ起動

```
$ docker-compose up -d
$ docker-compose ps                                                                    master ◼
  Name                Command               State            Ports
---------------------------------------------------------------------------
api        poetry run uvicorn app.mai ...   Up      0.0.0.0:8000->8000/tcp
postgres   docker-entrypoint.sh postgres    Up      5432/tcp
```

### データベースの初期化

```
$ docker exec -it -e PYTHONPATH="/app:$PYTHONPATH" api poetry run python app/init_db.py
```

#### 作成された DB の確認

```
$ docker-compose exec db psql -U postgres testdb
```

テーブルの確認。

```
# \dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)
```

レコードの確認。

```
# select * from users;
 id |  name   |                             password                             |        email        |         created_at         |         updated_at
----+---------+------------------------------------------------------------------+---------------------+----------------------------+----------------------------
  1 | squid   | 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | squid@example.com   | 2020-12-29 21:03:09.169173 | 2020-12-29 21:03:09.169173
  2 | octopus | 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | octopus@example.com | 2020-12-29 21:03:09.173484 | 2020-12-29 21:03:09.173484
(2 rows)
```

http://127.0.0.1:8000/docs へアクセス。

## テスト実行

```
$ pytest
```

## プロジェクトの構造

```
app
├── api                - API関連
│   └── v1             - API v1関連
│       └── endpoints  - APIのエンドポイントに関する処理
├── core               - configやロガーなど
├── domains            - Enterprise Business Rules
├── exceptions         - 例外
├── injector           - 依存性注入
├── interfaces         - Interface Adapters
│   └── gateways       - DB等の外部資源とのやりとりを行う
└── usecases           - Application Business Rules
    └── users          - ユーザ操作系処理
```

## 参考

- [FastAPI](https://fastapi.tiangolo.com/)
  - [tiangolo/fastapi (Github)](https://github.com/tiangolo/fastapi)
  - [tiangolo/full-stack-fastapi-postgresql (Github)](https://github.com/tiangolo/full-stack-fastapi-postgresql)
  - [nsidnev/fastapi-realworld-example-app (Github)](https://github.com/nsidnev/fastapi-realworld-example-app)
- [Starlette](https://www.starlette.io/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
