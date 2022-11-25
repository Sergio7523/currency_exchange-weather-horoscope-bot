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