import os
from quart import Quart
from quart_schema import QuartSchema
from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer


# APP SETTINGS
app = Quart(__name__)
QuartSchema(app, title="PytorchTTS APP", version="0.0.1")

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
from quart_tts_app.api.views import blueprint
app.register_blueprint(blueprint)

# COMMANDS
from quart_tts_app.api.commands import test_async
app.cli.add_command(test_async)

