from functools import wraps
import sqlite3 as db

from constants import ALLOWED_USERS, BOT_OWNER, USERS


class ValueSetter:

    def __set_name__(self, owner, name):
        self.name = '_' + name

    def __get__(self, instance, owner):
        return getattr(instance, self.name)

    def __set__(self, instance, value):
        return setattr(instance, self.name, value)


class Users:

    name = ValueSetter()
    last_name = ValueSetter()
    weather = ValueSetter()
    horoscope = ValueSetter()
    currency = ValueSetter()

    def __init__(
            self,
            name=None,
            last_name=None,
            weather=False,
            horoscope=False,
            currency=False
    ):
        self.name = name
        self.last_name = last_name
        self.weather = weather
        self.horoscope = horoscope
        self.currency = currency

    def reset(self):
        self.weather = False
        self.horoscope = False
        self.currency = False

    def __str__(self):
        return (
            f'Пользователь {self.name} {self.last_name}'
            if self.last_name else f'Пользователь {self.name}'
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
