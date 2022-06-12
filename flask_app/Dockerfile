FROM python:3.9-slim

RUN mkdir "flaskapp"
COPY requirements.txt flaskapp/requirements.txt
RUN pip install -U pip
RUN pip install -r flaskapp/requirements.txt
COPY . /flaskapp

ENV FLASK_ENV=development
ENV FLASK_APP=flaskapp.app:app

ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5003
EXPOSE 5003

ENTRYPOINT ["flask"]
CMD ["run", "--reload"]
