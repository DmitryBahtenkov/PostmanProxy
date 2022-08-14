from flask import Flask, Response, request
from postman import Postman, MonitorInfo
from config import Config
from telegram import Telegram

CFG_FILE = 'cfg.json'
CFG_TELEGRAM_KEY = 'telegram_key'
CFG_TELEGRAM_CHAT = 'telegram_chat'
CFG_POSTMAN_KEY = 'postman_key'
CFG_AUTH_KEY = 'secret_token'

REQUEST_AUTH_KEY = 'X-AUTH'

app = Flask(__name__)

cfg = Config(file=CFG_FILE)
postman = Postman(api_key=cfg.get(CFG_POSTMAN_KEY))
telegram = Telegram(api_key=cfg.get(CFG_TELEGRAM_KEY))


@app.route('/')
def index() -> Response:
    return Response(status=200)


@app.route('/data/<string:guid>', methods=['POST'])
def data(guid: str) -> str:
    try:
        if request.headers.get(REQUEST_AUTH_KEY) != cfg.get(CFG_AUTH_KEY):
            return 'Unauthorized'

        monitor: MonitorInfo = postman.get_monitor(guid=guid)
        telegram.send_message(
            chat_id=cfg.get(CFG_TELEGRAM_CHAT),
            message=str(monitor))

        return 'Ok'
    except ValueError as err:
        return err.args[0]


if __name__ == '__main__':
    app.run(host='localhost')
