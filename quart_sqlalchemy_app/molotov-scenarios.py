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

url = "http://localhost:5004"


@scenario(weight=60)
async def quart_app_scenario_one(session):
    async with session.get(f"{url}/posts/all") as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=60)
async def quart_app_scenario_two(session):
    data = json.dumps({"user_id": "molotov", "text": text(10)})
    async with session.post(f"{url}/posts/create", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status in [200, 404]


@scenario(weight=40)
async def quart_app_scenario_three(session):
    data = json.dumps({"user_id": "molotov"})
    async with session.post(f"{url}/posts/posts", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_four(session):
    data = json.dumps({"id": "molotov"})
    async with session.delete(f"{url}/posts/delete", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_five(session):
    async with session.get(f"{url}/users/all") as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=20)
async def quart_app_scenario_six(session):
    data = json.dumps({"id": "molotov", "username": text(5), "email": email(), "password": text(5), "picture": text(5)})
    async with session.put(f"{url}/users/update", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status in [200, 404]


@scenario(weight=20)
async def quart_app_scenario_seven(session):
    data = json.dumps({"id": "molotov"})
    async with session.post(f"{url}/users/user", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status in [200, 404]


@scenario(weight=30)
async def quart_app_scenario_eight(session):
    data = json.dumps({"username": text(5), "email": email(), "password": text(5), "picture": text(5)})
    async with session.post(f"{url}/users/create", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200


@scenario(weight=10)
async def quart_app_scenario_nine(session):
    data = json.dumps({"id": "molotov"})
    async with session.delete(f"{url}/users/delete", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200
