FROM python:3.8-alpine

RUN adduser -D microblog

WORKDIR /home/pp

COPY requirements.txt requirements.txt
COPY main.py config.py telegram.py postman.py cfg.json ./

RUN python -m venv venv
RUN venv/bin/pip3 install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "main.py", "run", "--host=0.0.0.0"]