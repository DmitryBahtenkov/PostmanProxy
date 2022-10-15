from flask import Flask, Response, request
from postman import Postman, MonitorInfo
from config import Config
from telegram import Telegram
from tp import TargetProcess
from utils import build_telegram_message

CFG_FILE = 'cfg.json'
CFG_TELEGRAM_KEY = 'telegram_key'
CFG_TELEGRAM_CHAT = 'telegram_chat'
CFG_TP_URL = 'tp_url'
CFG_TP_TOKEN = 'tp_access_token'

REQUEST_POSTMAN_KEY = 'X-POSTMAN_KEY'
CFG_AUTH_KEY = 'secret_token'

REQUEST_AUTH_KEY = 'X-AUTH'

app = Flask(__name__)

cfg = Config(file=CFG_FILE)
postman = Postman()
telegram = Telegram(api_key=cfg.get(CFG_TELEGRAM_KEY))
tp = TargetProcess(cfg.get(CFG_TP_URL), cfg.get(CFG_TP_TOKEN))

@app.route('/')
def index() -> Response:
    return Response(status=200)


@app.route('/data/<string:guid>', methods=['POST'])
def data(guid: str) -> str:
    try:
        if request.headers.get(REQUEST_AUTH_KEY) != cfg.get(CFG_AUTH_KEY):
            return 'Unauthorized'
        postman_key = request.headers.get(REQUEST_POSTMAN_KEY)

        monitor: MonitorInfo = postman.get_monitor(guid=guid, api_key=postman_key)
        last_release = tp.get_last_release('Name', 'Core')

        telegram.send_message(
            chat_id=cfg.get(CFG_TELEGRAM_CHAT),
            message=build_telegram_message(monitor, last_release, request.args.items()))

        return 'Ok'
    except ValueError as err:
        return err.args[0]


if __name__ == '__main__':
    app.run(host='0.0.0.0')
