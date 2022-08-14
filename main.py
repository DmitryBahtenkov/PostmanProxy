from flask import Flask, Response
from postman import Postman, MonitorInfo
from config import Config
from telegram import Telegram

CFG_FILE = 'cfg.json'
CFG_TELEGRAM_KEY = 'telegram_key'
CFG_TELEGRAM_CHAT = 'telegram_chat'
CFG_POSTMAN_KEY = 'postman_key'

app = Flask(__name__)

cfg = Config(file=CFG_FILE)
postman = Postman(api_key=cfg.get(CFG_POSTMAN_KEY))
telegram = Telegram(api_key=cfg.get(CFG_TELEGRAM_KEY))


@app.route('/')
def index() -> Response:
    return Response(status=200)


@app.route('data/<guid:str>', methods=['POST'])
def data(guid: str) -> str:
    try:
        monitor: MonitorInfo = postman.get_monitor(guid=guid)
        telegram.send_message(
            chat_id=cfg.get(CFG_TELEGRAM_CHAT),
            message=str(monitor))

        return 'Ok'
    except ValueError as err:
        return err.args[0]

