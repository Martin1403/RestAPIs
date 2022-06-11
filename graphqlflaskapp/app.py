import os
from flask import Flask

# FOLDERS CONFIG
BASE = os.path.abspath(os.path.join(os.path.dirname(__name__), "graphqlflaskapp"))
DATABASE_FOLDER = os.path.join(BASE, "database")
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# APP CONFIG
app = Flask(__name__)
app.config["SECRET_KEY"] = "somekey"
app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:////{DATABASE_FOLDER}/test.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# CLI COMMANDS
from graphqlflaskapp.api.tests import init_db, test_db, dal_adapter
app.cli.add_command(init_db)
app.cli.add_command(test_db)
app.cli.add_command(dal_adapter)

# MIGRATE DATABASE
from flask_migrate import Migrate
from graphqlflaskapp.api.models import db
Migrate(app, db, directory=os.path.join(BASE, "migrations"))


# BLUEPRINTS
from graphqlflaskapp.api.blueprint import blueprint
app.register_blueprint(blueprint)
