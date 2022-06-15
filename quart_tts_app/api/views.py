from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer
from quart import Blueprint, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass
from quart_tts_app.api.actions import action_endpoint


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
@action_endpoint
async def post(data: TextSchema):
    """Text to speech.
    The function returns list of floating point numbers representing wav.
    """
    return data
