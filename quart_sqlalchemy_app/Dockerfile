FROM python:3.9-slim

# App name
ARG APP="quart_sqlalchemy_app"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

# Settings:
ENV DOCKER=1
ENV QUART_APP=$APP.app:app
ENV QUART_ENV=development
EXPOSE 5010

CMD quart init-db && quart run -h "0.0.0.0" -p 5010