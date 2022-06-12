from typing import List
from dataclasses import asdict

from quart import Blueprint, render_template, redirect, jsonify
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer

from quart_app.app import app
from quart_app.api.actions import action_endpoint
from quart_app.api.dal import post_dal

post_blueprint = Blueprint("post_blueprint", __name__)


@dataclass
class PostSchema:
    """Post"""
    id: str
    user_id: str
    text: str
    date: str


@dataclass
class PostsSchema:
    """List Post"""
    posts: List[PostSchema]


@post_blueprint.route("/posts")
@validate_response(PostsSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/posts"})
@inprogress(app.api_requests_gauge, labels={"path": "/posts"})
async def posts_handler():
    """Posts
    The function return list of posts.
    """
    async with post_dal() as pd:
        posts = await pd.get_posts()
    return {"posts": posts}, 200
