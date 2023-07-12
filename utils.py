from functools import wraps
import sqlite3 as db

from constants import ALLOWED_USERS, BOT_OWNER, USERS


class Users:

    def __init__(
            self,
            name=None,
            last_name=None,
            weather=False,
            horoscope=False,
            currency=False
    ):
        self.__name = name
        self.__last_name = last_name
        self.__weather = weather
        self.__horoscope = horoscope
        self.__currency = currency

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        self.__name = value

    @property
    def last_name(self):
        return self.__last_name

    @last_name.setter
    def last_name(self, value):
        self.__last_name = value

    @property
    def weather(self):
        return self.__weather

    @weather.setter
    def weather(self, value):
        self.__weather = value

    @property
    def horoscope(self):
        return self.__horoscope

    @horoscope.setter
    def horoscope(self, value):
        self.__horoscope = value

    @property
    def currency(self):
        return self.__currency

    @currency.setter
    def currency(self, value):
        self.__currency = value

    def reset(self):
        self.__weather = False
        self.__horoscope = False
        self.__currency = False

    def __str__(self):
        return (
            f'Пользователь {self.__name} {self.last_name}'
            if self.__last_name else f'Пользователь {self.__name}'
        )


def get_chat_id(update):
    return str(update.effective_chat.id)


def get_username(update):
    return update.message.chat.first_name, update.message.chat.last_name


def reset(chat_id):
    USERS.get(chat_id).reset()


def create_db():
    with db.connect('bot_db.db') as con:
        cur = con.cursor()
        cur.execute(
            """CREATE TABLE IF NOT EXISTS users(
            chat_id TEXT,
            name TEXT,
            last_name TEXT,
            CONSTRAINT chat_id_unique UNIQUE (chat_id)
            );"""
        )


def restricted_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        chat_id = get_chat_id(args[0])
        if str(chat_id) in ALLOWED_USERS:
            return func(*args, **kwargs)
        else:
            message = 'У вас нет доступа к этому боту.'
            if func.__name__ != 'wake_up':
                message = (
                    'У вас нет доступа к этой функции.\n'
                    'Для получения доступа отправьте ID чата владельцу бота:\n'
                    f'{BOT_OWNER}\n'
                    'Ваш ID можно узнать нажав /user_info.'
                )
            args[1].bot.send_message(
                chat_id=chat_id,
                text=message
            )
    return wrapper


def add_user_to_db(user):
    with db.connect('bot_db.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO users VALUES(?, ?, ?)', user)
    add_users_to_dictionary()


def get_users_from_db():
    with db.connect('bot_db.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM users')
        result = cur.fetchall()
    return result


def add_users_to_dictionary():
    users = get_users_from_db()
    if len(users):
        for user in users:
            chat_id, name, last_name = user
            usr = Users(name, last_name)
            if chat_id not in USERS:
                USERS[chat_id] = usr


def update_db(user):
    chat_id, name, last_name = user
    with db.connect('bot_db.db') as con:
        cur = con.cursor()
        sql_update_query = (
            """UPDATE users SET name = ?, last_name = ? WHERE chat_id = ?"""
        )
        data = (name, last_name, chat_id)
        cur.execute(sql_update_query, data)
