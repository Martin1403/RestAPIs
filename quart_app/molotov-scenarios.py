import string
from random import choice
import json
import uuid

import shortuuid
from molotov import scenario


def text(x):
    return "".join([choice(string.ascii_lowercase) for _ in range(x)])


def password(x):
    return "".join([choice(string.digits) for _ in range(x)])


def email():
    return f"{text(10)}@{text(10)}.{text(3)}"


def generate_uuid():
    return shortuuid.encode(uuid.uuid4())


headers = {'accept': 'application/json',
           'Content-Type': 'application/json'}


@scenario(weight=20)
async def quart_app_scenario_one(session):
    async with session.get("http://localhost:5007/posts/all") as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_two(session):
    data = json.dumps({"user_id": generate_uuid(), "text": text(10)})
    async with session.post("http://localhost:5007/posts/create", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_three(session):
    data = json.dumps({"user_id": generate_uuid()})
    async with session.post("http://localhost:5007/posts/posts", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_four(session):
    data = json.dumps({"id": "molotov"})
    async with session.delete("http://localhost:5007/posts/delete", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_five(session):
    async with session.get("http://localhost:5007/users/all") as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_six(session):
    data = json.dumps({"id": "molotov", "username": text(5), "email": email(), "password": text(5), "picture": text(5)})
    async with session.put("http://localhost:5007/users/update", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_seven(session):
    data = json.dumps({"id": "molotov"})
    async with session.post("http://localhost:5007/users/user", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_eight(session):
    data = json.dumps({"username": text(5), "email": email(), "password": text(5), "picture": text(5)})
    async with session.post("http://localhost:5007/users/create", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_nine(session):
    data = json.dumps({"id": "molotov"})
    async with session.delete("http://localhost:5007/users/delete", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200
