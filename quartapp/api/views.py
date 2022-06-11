from quart import Blueprint, render_template, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from quartapp.api.actions import action_endpoint


blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
@hide_route
async def index():
    # return await render_template("index.html")
    return redirect("/docs")


@dataclass
class ToDoSchema:
    text: str


@blueprint.route("/get")
@validate_response(ToDoSchema)
async def get():
    return ToDoSchema(text="HelloWorld!!!")


@blueprint.route("/post", methods=["POST"])
@validate_request(ToDoSchema)
@validate_response(ToDoSchema)
@action_endpoint
async def post(data: ToDoSchema):
    return data
