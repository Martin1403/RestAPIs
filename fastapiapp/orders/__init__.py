from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from orders.api.models import Base, engine

app = FastAPI(debug=True, description="Example REST-API for orders.")
app.mount("/static", StaticFiles(directory="static"), name="static")
Base.metadata.create_all(bind=engine)

from orders.api import api
