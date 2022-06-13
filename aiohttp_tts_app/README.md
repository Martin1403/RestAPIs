Aiohttp TTS Pytorch app ![](static/images/logo.png)
=======================
![](static/images/screen.png)
### Venv:
###### python3.9
###### /aiohttp_tts_app
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Unpack voices:
```
apt-get install p7zip-full
7za x aiohttp_tts_app/voices/voices.7z.001 -oaiohttp_tts_app/voices/
```
[Audio](https://github.com/Martin1403/RestAPIs/blob/master/aiohttp_tts_app/templates/base.html)
### Run:
###### /
```
adev runserver ./aiohttp_tts_app \                                                                           1 ⨯
  --host "127.0.0.1" \
  --port 5000 \
  --livereload
```









### Tests:
###### /
- ###### Molotov
    ```
    molotov molotov.py -p 4 -w 5 -d 60
    ```
- ###### Init db
    ```
    python app.py --mode init
    ```
- ###### Test dal
    ```
    python app.py --mode dal
    ```  
### Docker:
###### /aiohttp_app
```
docker build -t aiohttp_app . && \
docker run -it --rm -p 5000:5000 aiohttp_app && \
docker rmi aiohttp_app --force
```
**Note:** Swagger file in config directory.
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link]()