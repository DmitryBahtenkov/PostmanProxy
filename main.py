from flask import Flask, Response, Request
from postman import Postman, MonitorInfo

app = Flask(__name__)
postman = Postman

@app.route('/')
def index() -> Response:
    return Response(status=200)


@app.route('data/<guid:str>', methods=['POST'])
def data(guid: str) -> str:
    try:
        monitor: MonitorInfo = postman.get_monitor(guid=guid)
    except ValueError as err:
        return err.args[0]
