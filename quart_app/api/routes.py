from quart import Blueprint, render_template, redirect
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer

from quart_app.app import app
from quart_app.api.actions import action_endpoint


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


@app.route("/posts")
@timer(app.request_timer, labels={"path": "/endpoint1"})
@inprogress(app.api_requests_gauge, labels={"path": "/endpoint1"})
async def endpoint1():
    #user = dict(username=text(20), email=email(), password=password(5))
    #async with user_dal() as ud:
    #    user = await ud.create_user(user)
    #return jsonify({"data": "endpoint1"})
    return {}
