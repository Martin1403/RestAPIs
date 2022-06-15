from aioprometheus import render, timer, inprogress
from quart import request, redirect, Blueprint
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass
from quart_tts_app.api.actions import action_endpoint

from quart_tts_app.app import app

blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
@hide_route
async def index():
    return redirect("/docs")


@dataclass
class TextSchema:
    """Text data."""
    data: str


@dataclass
class DataSchema:
    """Speech data."""
    data: str
    rate: int


@blueprint.route("/tts", methods=["POST"])
@validate_request(TextSchema)
@validate_response(DataSchema)
@timer(app.request_timer, labels={"path": "/tts"})
@inprogress(app.api_requests_gauge, labels={"path": "/tts"})
@action_endpoint
async def post(data: TextSchema):
    """Text to speech.
    The function returns list of floating point numbers representing wav.
    """
    return data
