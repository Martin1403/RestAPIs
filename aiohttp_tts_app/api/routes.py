from concurrent.futures import ThreadPoolExecutor
import base64
import io
import json
import os
from typing import Optional, Any, Dict

from aiohttp import web

from aiohttp_tts_app.api.lib import TTS
from aiohttp_tts_app.api.lib import InferenceBackend
from aiohttp_tts_app.api.lib.wavfile import write

routes = web.RouteTableDef()

max_thread_workers: Optional[int] = None
tts_settings: Dict[str, Any] = {"noise_scale": 0.667, "length_scale": 1.0}
vocoder_settings: Dict[str, Any] = {"denoiser_strength": 0.005}

backend = InferenceBackend("pytorch")
executor = ThreadPoolExecutor(max_workers=max_thread_workers)
tts = TTS(voice_or_lang="kathleen-glow_tts",
          vocoder_or_quality="low",  # "high", "medium", "low"
          backend="pytorch",
          tts_settings=tts_settings,
          vocoder_settings=vocoder_settings,
          executor=executor,
          denoiser_strength=vocoder_settings["denoiser_strength"],
          custom_voices_dir="aiohttp_tts_app/voices",
          )


@routes.route(method="GET", path="/")
async def handle(request):
    return web.HTTPFound('/docs')


"""EXAMPLE GET
@routes.route(method="GET", path="/hello/world")
async def hello_world(request):
    # import jinja2
    # import aiohttp_jinja2
    # context = {}
    # response = aiohttp_jinja2.render_template("base.html", request, context=context)
    # web.json_response(data={"data": "endpoint7"})
    return web.Response(text="Hello, world")
"""


@routes.route(method="POST", path="/tts")
async def tts_handler(request):
    response_bytes = await request.content.read()
    response_json = json.loads(response_bytes.decode("UTF-8"))
    text = response_json.get('text')
    tts_results = tts.text_to_speech(text=text)
    for result_idx, result in enumerate(tts_results):
        with io.BytesIO() as wav_io:
            write(wav_io, result.sample_rate, result.audio)
            wav_data = wav_io.getvalue()
            data = base64.encodebytes(wav_data).decode('ascii')
            if response_json.get('write'):
                path = "aiohttp_tts_app/samples/test.wav"
                if os.path.exists(path):
                    os.remove(path)
                with open(path, mode='bx') as f:
                    f.write(wav_data)
    return web.json_response(data={"data": data})
