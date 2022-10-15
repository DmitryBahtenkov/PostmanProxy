import telebot


class Telegram:
    def __init__(self, api_key: str):
        self._bot = telebot.TeleBot(api_key)

    def send_message(self, chat_id: str, message: str):
        result = self._bot.send_message(chat_id, message, parse_mode='HTML')
        print(result)
