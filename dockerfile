FROM python:3.8-alpine

RUN adduser -D postman

WORKDIR /home/pp

COPY requirements.txt requirements.txt
COPY main.py config.py telegram.py postman.py cfg.json ./
USER postman
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD [ "python3", "main.py", "run"]