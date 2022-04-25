import os
import time

import requests
import telegram
from dotenv import load_dotenv


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
    load_dotenv()
    dvmn_api = os.getenv('DVMN_API')
    telegram_api = os.getenv('TELEGRAM_API')
    chat_id = os.getenv('CHAT_ID')
    timestamp = time.time()
    bot = telegram.Bot(token=telegram_api)
    while True:
        try:
            checklist = get_checklist(dvmn_api, timestamp)
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            time.sleep(60)
        timestamp = get_timestamp(checklist)
        if checklist.get('status') == 'found':
            send_massage(bot, chat_id, checklist.get('new_attempts'))


if __name__ == '__main__':
    main()
