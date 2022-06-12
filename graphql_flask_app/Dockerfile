FROM python:3.9-slim

ARG APP="graphqlflaskapp"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

ENV FLASK_ENV=development
ENV FLASK_APP=$APP.app:app

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5004
EXPOSE 5004

ENTRYPOINT ["flask"]
CMD ["run", "--reload"]