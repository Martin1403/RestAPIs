import datetime
from random import choice
from typing import List
from dataclasses import asdict

from quart import Blueprint, render_template, redirect, jsonify
from quart_schema import hide_route, validate_request, validate_response
from pydantic.dataclasses import dataclass

from aioprometheus import Gauge, Registry, Summary, inprogress, render, timer

from quart_app.app import app
from quart_app.api.dal import user_dal

user_blueprint = Blueprint("user_blueprint", __name__, url_prefix="/users")


@dataclass
class NoContentSchema:
    """No Content"""
    pass


@dataclass
class IdSchema:
    """Id"""
    id: str


@dataclass
class CreateUserSchema:
    """Create User"""
    email: str
    password: str
    picture: str
    username: str


@dataclass
class UpdateUserSchema(IdSchema, CreateUserSchema):
    """Update user"""
    pass


@dataclass
class UserSchema(IdSchema):
    """User"""
    username: str
    email: str
    password_hash: str
    date: datetime.datetime
    picture: str


@dataclass
class UsersSchema:
    """List of users"""
    users: List[UserSchema]


@user_blueprint.route("/all")
@validate_response(UsersSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/users/all"})
@inprogress(app.api_requests_gauge, labels={"path": "/users/all"})
async def get_all_users_handler():
    """Get all users
    The function returns all users.
    """
    async with user_dal() as ud:
        users = await ud.get_users()
    return {"users": users}, 200


@user_blueprint.route("/create", methods=["POST"])
@validate_request(CreateUserSchema)
@validate_response(UserSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/users/create"})
@inprogress(app.api_requests_gauge, labels={"path": "/users/create"})
async def create_user_id_handler(data):
    """Create User
    The function Creates User.
    """
    async with user_dal() as ud:
        user = await ud.create_user(asdict(data))
    return user.json(), 200


@user_blueprint.route("/user", methods=["POST"])
@validate_request(IdSchema)
@validate_response(UserSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/users/user"})
@inprogress(app.api_requests_gauge, labels={"path": "/users/user"})
async def get_user_id_handler(data):
    """Get User id
    The function returns User by id.
    """
    async with user_dal() as ud:
        if data.id == "molotov":
            id = choice(await ud.get_users()).get('id')
            data.id = id
        user = await ud.get_user_id(id=data.id)
    return user.json(), 200


@user_blueprint.route("/update", methods=["PUT"])
@validate_request(UpdateUserSchema)
@validate_response(UserSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/users/update"})
@inprogress(app.api_requests_gauge, labels={"path": "/users/update"})
async def update_user_id_handler(data: UpdateUserSchema):
    """Update User id
    The function updates User by id.
    """
    async with user_dal() as ud:
        if data.id == "molotov":
            id = choice(await ud.get_users()).get('id')
            data.id = id
        user = await ud.update_user(asdict(data))
    return user.json(), 200


@user_blueprint.route("/delete", methods=["DELETE"])
@validate_request(IdSchema)
@validate_response(NoContentSchema, status_code=200)
@timer(app.request_timer, labels={"path": "/users/delete"})
@inprogress(app.api_requests_gauge, labels={"path": "/users/delete"})
async def delete_user_id_handler(data: IdSchema):
    """Delete User id
    The function deletes User by id.
    """
    async with user_dal() as ud:
        if data.id == "molotov":
            id = choice(await ud.get_users()).get('id')
            data.id = id
        await ud.delete_user_id(id=data.id)
    return {}, 200
