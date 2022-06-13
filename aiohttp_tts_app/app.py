import os
import sys
import jinja2
import aiohttp_jinja2
from aiohttp import web
from aiohttp_prometheus_exporter.handler import metrics
from aiohttp_prometheus_exporter.middleware import prometheus_middleware_factory
from swagger_ui import api_doc
from aiohttp_tts_app.api.routes import routes


# APP SETTINGS
app = web.Application()
app.middlewares.append(prometheus_middleware_factory())
app.router.add_get("/metrics", metrics())


# REGISTER BLUEPRINT
app.router.add_routes(routes)

aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader(os.path.join(os.getcwd(), "templates")))
api_doc(app, config_path='./aiohttp_tts_app/api/docs.yaml', url_prefix='/docs', title='API doc')
# api_doc(app, config_path='./aiohttp_tts_app/api/petstore.yaml', url_prefix='/docs', title='API doc')

if __name__ == '__main__':
    pass
