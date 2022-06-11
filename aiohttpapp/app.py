import os
import jinja2
import aiohttp_jinja2
from aiohttp import web
from swagger_ui import api_doc

routes = web.RouteTableDef()


@routes.route(method="GET", path="/")
async def handle(request):
    context = {}
    # response = aiohttp_jinja2.render_template("base.html", request, context=context)
    return web.HTTPFound('/docs')


@routes.route(method="GET", path="/hello/world")
async def hello_world(request):
    return web.Response(text="Hello, world")


app = web.Application()
app.router.add_routes(routes)
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")))
api_doc(app, config_path='./config/test.yaml', url_prefix='/docs', title='API doc')

