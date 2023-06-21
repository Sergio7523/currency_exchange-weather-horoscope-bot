## Описание проекта

Бот для Telegram.
Бот может:
- Прислать погоду в выбранном городе. Делается запрос на API сервер погоды.
- Прислать горосккоп на текущую день. Бот парсит сайт гороскопа и выдает результат пользователю.
- Конвертировать валюту. Доступно 43 валюты. Конвертация возможна между всеми волютами из доступных.
- Прислать случайную фотографию кошки или собаки.
___

### Технологии
- Python 3.10
- python-telegram-bot==13.14
- sqlite3
- beautifulsoup4
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
