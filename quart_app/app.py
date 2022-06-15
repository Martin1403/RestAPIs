import asyncio
from random import choice

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer
from quart import Quart
from quart_schema import QuartSchema


# APP SETTINGS
app = Quart(__name__)
QuartSchema(app, title="QUART APP", version="0.0.1")

# PROMETHEUS
app.registry = Registry()
app.api_requests_gauge = Gauge(
    "quart_active_requests",
    "Number of active requests per endpoint"
)
app.request_timer = Summary(
    "request_processing_seconds",
    "Time spent processing request"
)
app.registry.register(app.api_requests_gauge)
app.registry.register(app.request_timer)

# REGISTER BLUEPRINTS
from quart_app.api.routes.base import base_blueprint
from quart_app.api.routes.posts import post_blueprint
from quart_app.api.routes.users import user_blueprint
app.register_blueprint(base_blueprint)
app.register_blueprint(post_blueprint)
app.register_blueprint(user_blueprint)


# COMMANDS
from quart_app.api.commands import test_async, init_db, test_dal
app.cli.add_command(test_async)
app.cli.add_command(init_db)
app.cli.add_command(test_dal)

