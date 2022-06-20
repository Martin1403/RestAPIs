import datetime
from random import choice
from typing import List, Union, Tuple, Optional, Any
from dataclasses import asdict

from quart import Blueprint
from quart_schema import validate_request, validate_response
from pydantic.dataclasses import dataclass

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer

from quart_sqlalchemy_app.app import app
from quart_sqlalchemy_app.api.dal import post_dal, user_dal

post_blueprint = Blueprint("post_blueprint", __name__, url_prefix="/posts")


@dataclass
class ErrorSchema:
    """Error handler"""
    error: str


@dataclass
class NoContentSchema:
    """No Content"""
    pass


@dataclass
class IdSchema:
    """PostId"""
    id: str


@dataclass
class UserIdSchema:
    """UserId"""
    user_id: str


@dataclass
class CreatePostSchema(UserIdSchema):
    """Create Post"""
    text: str


@dataclass
class PostSchema(CreatePostSchema):
    """Post"""
    id: str
    date: str


@dataclass
class PostsSchema:
    """List Post"""
    posts: Union[List[PostSchema], List]


@post_blueprint.route("/all")
@validate_response(PostsSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/posts/all"})
@inprogress(app.api_requests_gauge, labels={"path": "/posts/all"})
async def all_posts_handler():
    """Posts
    The function return list of posts.
    """

    async with post_dal() as pd:
        posts = await pd.get_posts()

    return {"posts": posts}, 200


@post_blueprint.route("/create", methods=["POST"])
@validate_request(CreatePostSchema)
@validate_response(PostSchema, status_code=200)
@validate_response(NoContentSchema, status_code=404)
@timer(app.request_timer, labels={"path": "/posts/create"})
@inprogress(app.api_requests_gauge, labels={"path": "/posts/create"})
async def create_post_handler(data):
    """Post
    The function create post by user id/
    """
    if data.user_id == "molotov":
        async with user_dal() as ud:
            users = await ud.get_users()
            if users:
                data.user_id = choice(users).get('id')

    async with post_dal() as pd:
        post = await pd.create_post_user_id(**asdict(data))

    return (post.json(), 200) if post else ({}, 404)


@post_blueprint.route("/posts", methods=["POST"])
@validate_request(UserIdSchema)
@validate_response(PostsSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/posts/posts"})
@inprogress(app.api_requests_gauge, labels={"path": "/posts/posts"})
async def get_posts_user_id_handler(data):
    """Get Posts id
    The function returns posts by user id.
    """
    if data.user_id == "molotov":
        async with user_dal() as ud:
            users = await ud.get_users()
            if users:
                data.user_id = choice(users).get('id')

    async with post_dal() as pd:
        posts = await pd.get_posts_user_id(data.user_id)

    return {"posts": posts}, 200


@post_blueprint.route("/delete", methods=["DELETE"])
@validate_request(IdSchema)
@validate_response(NoContentSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/posts/delete"})
@inprogress(app.api_requests_gauge, labels={"path": "/posts/delete"})
async def delete_post_id_handler(data):
    """Get Posts id
    The function returns posts by user id.
    """
    if data.id == "molotov":
        async with post_dal() as pd:
            posts = await pd.get_posts()
            if posts:
                data.id = choice(posts).get('id')

    async with post_dal() as pd:
        await pd.delete_post_id(id=data.id)

    return {}, 200
