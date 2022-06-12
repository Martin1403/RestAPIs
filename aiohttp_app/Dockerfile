FROM python:3.9-slim

# App name
ARG APP="aiohttp_app"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

WORKDIR $APP
# Settings:
EXPOSE 5000

CMD adev runserver --livereload --host "0.0.0.0" --port 5000 --livereload
