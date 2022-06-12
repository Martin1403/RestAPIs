Quart app ![](static/images/logo.png)
=========
![](static/images/screen.png)
### Venv:
###### python3.9
###### /quartapp
```
python -m venv .venv && \
source .venv/bin/activate && \
pip install -U pip && \
pip install -r requirements.txt
```
### Run:
###### /
```
export QUART_APP=quartapp.app:app && \
export QUART_ENV=development && \
quart run -h "127.0.0.1" -p 5007
```
### Tests:
###### /
- ###### Test async:
    ````
    export QUART_APP=quartapp.app:app && \
    export QUART_ENV=development && \
    quart test-async
    ````
### Docker:
###### /quartapp
```
docker build -t quartapp . && \
docker run -it --rm -p 5007:5007 quartapp && \
docker rmi quartapp --force
```
**Note:** 
###### Help:
- ###### / inside root directory or cd /xxx  
###### [Links:]()
- ###### [Link]()