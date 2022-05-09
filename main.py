from decimal import DivisionByZero
import logging
import os
import time

import requests
import telegram
from dotenv import load_dotenv


logger = logging.getLogger('Logger')

class TelegramLogsHandler(logging.Handler):

    def __init__(self, bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.main = bot

    def emit(self, record):
        log_entry = self.format(record)
        self.main.send_message(chat_id=self.chat_id, text=log_entry)


def get_checklist(dvmn_api, timestamp):
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {dvmn_api}'}
    payload = {'timestamp': timestamp}
    response = requests.get(url, headers=headers, params=payload)
    response.raise_for_status()
    return response.json()


def get_timestamp(checklist):
    if checklist.get('status') == 'found':
        return checklist.get('last_attempt_timestamp')
    else:
        return checklist.get('timestamp_to_request')


def send_massage(bot, chat_id, attempts):
    for attempt in attempts:
        if attempt.get('is_negative'):
            text = (f"❌ Задание {attempt.get('lesson_title')} не принято"
                    f"\n{attempt.get('lesson_url')}")
        else:
            text = f"✅ Задание {attempt.get('lesson_title')} принято"
        bot.send_message(text=text, chat_id=chat_id)


def main():
    logging.basicConfig(level=logging.DEBUG)
    logger.setLevel(logging.DEBUG)
    load_dotenv()
    dvmn_api = os.getenv('DVMN_API')
    telegram_api = os.getenv('TELEGRAM_API')
    chat_id = os.getenv('CHAT_ID')
    timestamp = time.time()
    bot = telegram.Bot(token=telegram_api)
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('The ragnhild bot is running')
    while True:
        try:
            checklist = get_checklist(dvmn_api, timestamp)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            logger.error('Connection error...')
            time.sleep(60)
            continue
        timestamp = get_timestamp(checklist)
        if checklist.get('status') == 'found':
            send_massage(bot, chat_id, checklist.get('new_attempts'))


if __name__ == '__main__':
    main()
