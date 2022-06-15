from quart import Blueprint, request, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer
from quart_app.app import app

base_blueprint = Blueprint("base_blueprint", __name__)


@app.route("/")
@hide_route
async def index():
    # return await render_template("index.html")
    return redirect("/docs")


@app.route("/metrics")
@hide_route
async def handle_metrics():
    return render(app.registry, request.headers.getlist("accept"))

