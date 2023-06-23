from functools import wraps
import psycopg2 as db

from constants import (
    ALLOWED_USERS, DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER
)


def get_chat_id(update):
    return update.effective_chat.id


def get_username(update):
    return update.message.chat.first_name, update.message.chat.last_name


def restricted_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        chat_id = get_chat_id(args[0])
        if chat_id in ALLOWED_USERS:
            return func(*args, **kwargs)
        else:
            message = 'У вас нет доступа к этому боту'
            if func.__name__ != 'wake_up':
                message = 'У вас нет доступа к этой функции'
            args[1].bot.send_message(
                chat_id=chat_id,
                text=message
            )
    return wrapper


def create_db():
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        create_users = (
                """CREATE TABLE IF NOT EXISTS users(
                chat_id INTEGER PRIMARY KEY,
                name VARCHAR(100),
                last_name VARCHAR(100)
                );"""
        )
        create_user_statuses = (
                """CREATE TABLE IF NOT EXISTS users_statuses(
                chat_id INTEGER REFERENCES users (chat_id) ON DELETE CASCADE,
                weather BOOL DEFAULT False,
                horoscope BOOL DEFAULT False,
                currency BOOL DEFAULT False
                );"""
        )
        with con.cursor() as cur:
            cur.execute(create_users)
            cur.execute(create_user_statuses)


def add_user_to_db(user):
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute(
                """INSERT INTO users
                VALUES(%s, %s, %s);""",
                user
            )
            cur.execute(
                """INSERT INTO users_statuses (chat_id)
                VALUES(%s);""",
                (user[0],)
            )


def update_db(user):
    chat_id, name, last_name = user
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            sql_update_query = (
                """UPDATE users
                SET name=%s, last_name=%s
                WHERE chat_id=%s;"""
            )
            data = (name, last_name, chat_id)
            cur.execute(sql_update_query, data)


def get_users_from_db():
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute('SELECT * FROM users;')
            result = cur.fetchall()
    return result


def update_weather(chat_id):
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute(
                """UPDATE users_statuses
                SET weather=%s
                WHERE chat_id=%s;""",
                (True, chat_id)
            )


def update_horoscope(chat_id):
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute(
                """UPDATE users_statuses
                SET horoscope=%s
                WHERE chat_id=%s;""",
                (True, chat_id)
            )


def update_currency(chat_id):
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute(
                """UPDATE users_statuses
                SET currency=%s
                WHERE chat_id=%s;""",
                (True, chat_id)
            )


def get_user_statuses(chat_id):
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute(
                """SELECT weather, horoscope, currency
                FROM users_statuses
                WHERE chat_id=%s;""", (chat_id,)
            )
            result = cur.fetchone()
    return result


def reset(chat_id):
    with db.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    ) as con:
        with con.cursor() as cur:
            cur.execute(
                """UPDATE users_statuses
                SET weather=%s, horoscope=%s, currency=%s
                WHERE chat_id=%s""",
                (False, False, False, chat_id,)
            )
