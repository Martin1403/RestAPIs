from random import choice
import json
from time import time
from molotov import scenario


headers = {'accept': 'application/json',
           'Content-Type': 'application/json'}


@scenario(weight=100)
async def quart_app_scenario_three(session):
    data = json.dumps({"data": "Hello, how are you today?"})
    async with session.post("http://localhost:5009/tts", data=data, headers=headers) as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200
