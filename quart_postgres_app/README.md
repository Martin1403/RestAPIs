REST API with Quart & Postgres ![](static/images/logo.png)
==============================
![](static/images/Swagger.png)
![](static/images/pgadmin4.png)
### Venv:
###### python3.9
###### /quart_postgres_app
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Run:
- ###### 1. ) /quart_postgres_app
```
docker run -p5432:5432 --name some-postgres \
  -e POSTGRES_PASSWORD=password -d postgres
```
- ###### 2. ) /quart_postgres_app
```
docker run -p 5555:80 --name pgadmin \
    -e PGADMIN_DEFAULT_EMAIL="user@domain.com" \
    -e PGADMIN_DEFAULT_PASSWORD="12345" \
    -d dpage/pgadmin4
```
- ###### 3. ) /
```
export QUART_APP=quart_postgres_app.app:app && \
export QUART_ENV=development && \
quart init-db && \
quart run -h "127.0.0.1" -p 5008
```
### Docker compose:
```
docker-compose up --build
```

**Note:** Databases ...
```
pip install databases[postgresql]
pip install databases[mysql]
pip install databases[sqlite]
pip install databases[asyncpg]
pip install databases[aiopg]
pip install databases[aiomysql]
pip install databases[asyncmy]
pip install databases[aiosqlite]
```
###### Help:
- ###### / inside root directory or cd /xxx
###### [Links:]()
- ###### [Link]()