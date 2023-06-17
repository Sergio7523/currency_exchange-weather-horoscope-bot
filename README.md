# **Kittybot**
___ 

## Описание проекта

Kittybot - бот для Telegram.
Делает запросы на API сервиса погоды и API с коллекцией фотографий животных
Показывает погоду в выбранном городе.
Присылает случайные фотографии кошек и собак
___

### Технологии
- Python 3.10
- python-telegram-bot==13.14
- sqlite3
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