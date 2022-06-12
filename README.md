REST-APIs
=========
![](logo.png)

- ###### [Aiohttp rest api](https://github.com/Martin1403/RestAPIs/tree/master/aiohttp_app) Simple api with Sqlite
- ###### [Django rest api](https://github.com/Martin1403/RestAPIs/tree/master/django_app) Simple api with Sqlite database
- ###### [FastApi rest api](https://github.com/Martin1403/RestAPIs/tree/master/fastapi_app) Simple api with Sqlite database
- ###### [Flask rest api](https://github.com/Martin1403/RestAPIs/tree/master/flask_app) Simple api with Sqlite database
- ###### [GraphQL Flask rest api](https://github.com/Martin1403/RestAPIs/tree/master/graphql_flask_app) Simple api with Sqlite database
- ###### [GraphQL quart rest api](https://github.com/Martin1403/RestAPIs/tree/master/graphql_quart_app) Simple api with Sqlite database
- ###### [GraphQL starlette rest api](https://github.com/Martin1403/RestAPIs/tree/master/graphql_starlette_app) Simple api
- ###### [Quart rest api](https://github.com/Martin1403/RestAPIs/tree/master/quartapp) Simple api
- ###### [Quart rest api with postgres](https://github.com/Martin1403/RestAPIs/tree/master/quart_postgres_app) Simple api with postgres database


### Run:
```
git clone https://github.com/Martin1403/RestAPIs.git && \
cd RestAPIs && \
docker-compose up --build && \
docker-compose down && \
docker rmi $(docker images --format="{{.ID}}" restapis_*) --force && \
docker volume prune && \
cd .. && \
rm -r RestAPIs
```

**Note:**
Run all services, Ctrl-C to end, confirm delete ...
