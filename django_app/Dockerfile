FROM python:3.9-slim

RUN mkdir djangoapp
RUN pip install -U pip
COPY requirements.txt djangoapp/requirements.txt
RUN pip install -r djangoapp/requirements.txt

COPY . djangoapp/
WORKDIR djangoapp/django_todo/

# Settings:
EXPOSE 5001

CMD python manage.py runserver 0.0.0.0:5001