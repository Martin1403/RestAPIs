from molotov import scenario
# Run:
# molotov molotov-scenarios.py -p 10 -w 200 -d 60


@scenario(weight=20)
async def scenario_one(session):
    async with session.get("http://localhost:5007/posts") as resp:
        res = await resp.json()
        assert type(res) == dict
        assert resp.status == 200
