## 概要

クリーンアーキテクチャ(Clean Architecture)で実装したFastAPIベースのシンプルな
ユーザ操作(CRUD)API。
## 開発環境構築

Pythonライブラリのインストール。

```
pip install poetry
```

## データベース初期化

### Postgresqlコンテナの作成

docker-composeの利用が前提となっているため、事前にインストールをしておくこと。

```
cd postgresql
docker-compose up -d
docker-compose ps
```

### DBを初期化

```
cd ..
export PYTHONPATH="$(pwd):$PYTHONPATH"
python app/init_db.py
```

### 作成されたDBの確認

```
cd postgresql
docker-compose exec db psql -U postgres testdb
```

テーブルの確認。

```
\dt
         List of relations
 Schema | Name  | Type  |  Owner
--------+-------+-------+----------
 public | users | table | postgres
(1 row)
```

レコードの確認。

```
select * from users;
 id |  name   |                             password                             |        email        |         created_at         |         updated_at
----+---------+------------------------------------------------------------------+---------------------+----------------------------+----------------------------
  1 | squid   | 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | squid@example.com   | 2020-12-29 21:03:09.169173 | 2020-12-29 21:03:09.169173
  2 | octopus | 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 | octopus@example.com | 2020-12-29 21:03:09.173484 | 2020-12-29 21:03:09.173484
(2 rows)
```