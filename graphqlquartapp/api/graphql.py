from quart import Blueprint, redirect
from ariadne import graphql
from ariadne.constants import PLAYGROUND_HTML
from quart import request, jsonify


from graphqlquartapp.api.schema import schema
from graphqlquartapp.app import app

blueprint = Blueprint("blueprint", __name__)


@blueprint.route("/")
async def index():
    return redirect("/graphql")


@blueprint.route("/graphql", methods=["GET"])
async def graphql_playground():
    """supplies playground environment"""
    return PLAYGROUND_HTML, 200


@blueprint.route("/graphql", methods=["POST"])
async def graphql_server():
    data = await request.get_json()
    success, result = await graphql(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )
    return jsonify(result), 200 if success else 400
