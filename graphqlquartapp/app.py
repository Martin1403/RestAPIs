import os
from quart import Quart, render_template

# APP SETUP
app = Quart(__name__)
app.config["BASE_FOLDER_PATH"] = os.path.abspath(os.path.join(os.path.dirname(__name__), "graphqlquartapp"))
app.config["DATABASE_FOLDER_PATH"] = os.path.join(app.config["BASE_FOLDER_PATH"], "database")
app.config["DATABASE_URI_PATH"] = os.path.join(app.config["DATABASE_FOLDER_PATH"], "test.db")
os.makedirs(app.config["DATABASE_FOLDER_PATH"], exist_ok=True)

# CLICK COMMANDS
from graphqlquartapp.api.tests.asyncrun import test_async
from graphqlquartapp.api.tests.initialize import init_db
from graphqlquartapp.api.tests.database import test_db
from graphqlquartapp.api.tests.dal import test_dal
app.cli.add_command(test_async)
app.cli.add_command(init_db)
app.cli.add_command(test_db)
app.cli.add_command(test_dal)


# REGISTER BLUEPRINTS
from graphqlquartapp.api.graphql import blueprint
app.register_blueprint(blueprint)
