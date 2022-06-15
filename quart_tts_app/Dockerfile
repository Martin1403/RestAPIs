FROM python:3.9-slim

# App name
ARG APP="quart_tts_app"

RUN mkdir $APP
COPY . /$APP
RUN pip install -U pip
RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install libopenblas-base libgomp1 libatomic1
RUN apt-get -y install p7zip-full
RUN pip install -r $APP/requirements.txt
RUN pip install torch==1.8.1+cpu torchvision==0.9.1+cpu torchaudio==0.8.1 -f https://download.pytorch.org/whl/lts/1.8/torch_lts.html
RUN 7za x quart_tts_app/voices/voices.7z.001 -oquart_tts_app/voices/

# Settings:
ENV QUART_APP=$APP.app:app
ENV QUART_ENV=development
EXPOSE 5009

CMD quart run -h "0.0.0.0" -p 5009