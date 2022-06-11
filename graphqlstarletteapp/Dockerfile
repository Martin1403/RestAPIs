FROM python:3.9-slim

# App name
ARG APP="qraphqlstarletteapp"

RUN mkdir $APP
COPY requirements.txt $APP/requirements.txt
RUN pip install -U pip
RUN pip install -r $APP/requirements.txt
COPY . /$APP

# Settings:
EXPOSE 5006

CMD uvicorn qraphqlstarletteapp.app:app --host 0.0.0.0 --port 5006 --reload