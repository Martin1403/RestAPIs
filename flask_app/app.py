from flask import Flask
from flask_smorest import Api

from flaskapp.api.routes import blueprint
from flaskapp.config import BaseConfig
from flaskapp.api.models import Base, engine

app = Flask(__name__)

app.config.from_object(BaseConfig)

users_api = Api(app)

users_api.register_blueprint(blueprint)

Base.metadata.create_all(bind=engine)
