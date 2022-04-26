# ragnild

Telegram бот будет присылать уведомления о готовности проверки ваших работ с курсов [dvmn.org](https://dvmn.org/)

## Запуск бота

Для запуска программы требуется Python 3.

- Скачайте код `git clone https://github.com/dad-siberian/ragnild.git`
- Установите зависимости командой `pip install -r requirements.txt`
- Создать в корне проекта переменную окружения `.env` и внести настройки. Подробнее в разделе настройка переменной окружения.
- Запустите скрипт командой `python3 main.py`

## Настройка переменной окружения

```
DVMN_API={devman api}
TELEGRAM_API={Telegram api key}
CHAT_ID={chat_id}
```

- DVMN_API это ваш персональный токен API Девмана.
- создать телеграм бота у [@BotFather](https://telegram.me/BotFather) ([инструкция](https://botcreators.ru/blog/kak-sozdat-svoego-bota-v-botfather/)). Полученный token api необходимо присвоить переменной TELEGRAM_API.
- Чтобы получить свой `chat_id`, напишите в Telegram специальному боту: [@userinfobot](https://t.me/userinfobot) и присвойте переменной CHAT_ID

## Предварительные условия

Для работы скрипта у вас должен быть установлен python версии 3.8 и выше.

## Запуск бота на сервере

Для постоянной работы бота необходимо запустить на сервере, например на [Heroku: Cloud Application Platform](https://www.heroku.com).
На сайте есть подробная [инструкция](https://devcenter.heroku.com/articles/getting-started-with-python).


Переменные окружения передаются на сервер командой
```
heroku config:set DVMN_API={devman api}
```

Для работы с Heroku на территории РФ может понадобиться VPN

## Цель проекта

Получение уведомлений о готовности ревью кода
