from telebot import TeleBot


class Telegram:
    def __init__(self, api_key: str):
        self._bot = TeleBot(api_key)

    def send_message(self, chat_id: str, message: str):
        self._bot.send_message(chat_id=chat_id, text=message)
