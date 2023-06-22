## Описание проекта

Бот для Telegram.

Реализовано 2 версии. Для запуска без установок дополнительного П/О использовать ветку sqlite.
В ветке sqlite взаимодействие с БД сведено к минимуму.

Бот может:
- Прислать погоду в выбранном городе. Делается запрос на API сервер погоды.
- Прислать гороскоп на текущий день. Бот парсит сайт гороскопа и выдает результат пользователю.
- Конвертировать валюту. Доступно 43 валюты. Конвертация возможна между всеми волютами из доступных.
- Прислать случайную фотографию кошки или собаки.

Реализована возможность полносью ограничивать доступ к боту или его отдельному функционалу.
___

### Технологии

- Python 3.10
- python-telegram-bot==13.14
- postgresql (ветка main) / sqlite3 (ветка sqlite)
- Docker (ветка main)
___

## Установка

Cоздать и активировать виртуальное окружение:

Windows:

```sh
python -m venv env

source venv/scripts/activate
```
MacOs:
```sh
python3 -m venv env

source env/bin/activate
```

Установить зависимости из файла requirements.txt:

Windows:
```sh
python -m pip install --upgrade pip

pip install -r requirements.txt
```
MacOs:
```sh
python3 -m pip install --upgrade pip

pip install -r requirements.txt
```
___

## Запуск проекта в контейнере

Скачать и установить [Docker](https://www.docker.com/).
```sh
docker-compose up -d
```