Pytorch TTS API![](static/images/logo.png)
================
### Venv:
###### python3.9
###### /
```
python -m venv quart_tts_app/.venv && \
source quart_tts_app/.venv/bin/activate && \
pip install -U pip && \
pip install -r quart_tts_app/requirements.txt && \
pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
```
### Unpack voices:
###### / 
###### apt-get install p7zip-full
```
7za x quart_tts_app/voices/voices.7z.001 -oquart_tts_app/voices/
```
### Run:
###### /
```
export QUART_APP=quart_tts_app.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5009
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=quart_tts_app.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
- ###### Molotov:
    ````
    molotov molotov-scenarios.py \
    --processes 5 \
    --workers 2 \
    --duration 6
    ````  


### Docker:
###### /quart_tts_app
```
docker build -t quart_tts_app . && \
docker run -it --rm -p 5009:5009 quart_tts_app && \
docker rmi quart_tts_app --force
```
**Note:** 
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]() 
- ###### [Link](https://drive.google.com/drive/folders/10_ZNA4PxF3QtYrBBEwjAFQfnhH9E1yqY?usp=sharing) Download more voices
- ###### [Link](https://github.com/rhasspy/larynx) GitHub link to Larynx
