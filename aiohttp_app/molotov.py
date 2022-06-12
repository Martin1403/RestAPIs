from molotov import scenario
# molotov_example.py
# Run:
# molotov molotov_example.py -p 10 -w 200 -d 60


@scenario(weight=20)
async def scenario_one(session):
    async with session.get("http://localhost:5000/endpoint1") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint1"
        assert resp.status == 200


@scenario(weight=10)
async def scenario_two(session):
    async with session.get("http://localhost:5000/endpoint2") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint2"
        assert resp.status == 200


@scenario(weight=20)
async def scenario_three(session):
    async with session.get("http://localhost:5000/endpoint3") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint3"
        assert resp.status == 200


@scenario(weight=10)
async def scenario_four(session):
    async with session.get("http://localhost:5000/endpoint4") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint4"
        assert resp.status == 200


@scenario(weight=10)
async def scenario_five(session):
    async with session.get("http://localhost:5000/endpoint5") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint5"
        assert resp.status == 200


@scenario(weight=10)
async def scenario_six(session):
    async with session.get("http://localhost:5000/endpoint6") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint6"
        assert resp.status == 200


@scenario(weight=20)
async def scenario_seven(session):
    async with session.get("http://localhost:5000/endpoint7") as resp:
        res = await resp.json()
        assert res["data"] == "endpoint7"
        assert resp.status == 200
