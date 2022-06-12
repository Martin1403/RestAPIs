import random
import sys
from random import choice
from aiohttp import web
# import jinja2
# import aiohttp_jinja2
# response = aiohttp_jinja2.render_template("base.html", request, context=context)

from api.commands import text, password, email
from api.dal import user_dal, post_dal

routes = web.RouteTableDef()


@routes.route(method="GET", path="/")
async def handle(request):
    context = {}
    return web.HTTPFound('/docs')


@routes.route(method="GET", path="/hello/world")
async def hello_world(request):
    return web.Response(text="Hello, world")


@routes.route(method="GET", path="/endpoint1")
async def endpoint1(request):
    user = dict(username=text(20), email=email(), password=password(5))
    async with user_dal() as ud:
        user = await ud.create_user(user)
    return web.json_response(data={"data": "endpoint1"})


@routes.route(method="GET", path="/endpoint2")
async def endpoint2(request):
    async with user_dal() as ud:
        users = await ud.get_users()
        user = await ud.get_user_id(choice(users).id)
    return web.json_response(data={"data": "endpoint2"})


@routes.route(method="GET", path="/endpoint3")
async def endpoint3(request):
    async with user_dal() as ud:
        users = await ud.get_users()
        user = random.choice(users).json()
        if user:
            user["password"] = password(5)
            user["username"] = text(5)
            user["email"] = email()
            user["picture"] = text(10)
            user.pop("date")
            user = await ud.update_user(user)
    return web.json_response(data={"data": "endpoint3"})


@routes.route(method="GET", path="/endpoint4")
async def endpoint4(request):
    async with post_dal() as pd:
        async with user_dal() as ud:
            users = await ud.get_users()
        post = await pd.create_post_user_id(user_id=choice(users).id, text=text(10))
    return web.json_response(data={"data": "endpoint4"})


@routes.route(method="GET", path="/endpoint5")
async def endpoint5(request):
    async with post_dal() as pd:
        posts = await pd.get_posts()
        if posts:
            await pd.delete_post_id(choice(posts).id)
    return web.json_response(data={"data": "endpoint5"})


@routes.route(method="GET", path="/endpoint6")
async def endpoint6(request):
    async with user_dal() as ud:
        users = await ud.get_users()
        if users:
            await ud.delete_user_id(id=choice(users).id)
    return web.json_response(data={"data": "endpoint6"})


@routes.route(method="GET", path="/endpoint7")
async def endpoint7(request):
    async with post_dal() as pd:
        posts = await pd.get_posts()
        if posts:
            posts = await pd.get_posts_user_id(user_id=choice(posts).userId)
    return web.json_response(data={"data": "endpoint7"})
