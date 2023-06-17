import sqlite3 as db

from constants import USERS, ALLOWED_USERS

def get_chat_id(update):
    return str(update.effective_chat.id)

def get_username(update):
    return update.message.chat.first_name, update.message.chat.last_name

def reset(chat_id):
    for value in USERS.get(chat_id):
        if USERS[chat_id][value]:
            USERS[chat_id][value] = False

def create_db():
    with db.connect('kittybot_db.db') as con:
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
    def wrapper(*args, **kwargs):
        chat_id = get_chat_id(args[0])
        if chat_id in ALLOWED_USERS:
            return func(*args, **kwargs)
        else:
            args[1].bot.send_message(
                chat_id=chat_id,
                text='Доступ ограничен'
            )
    return wrapper

def add_user_to_db(user):
    with db.connect('kittybot_db.db') as con:
        cur = con.cursor()
        cur.execute('INSERT INTO users VALUES(?, ?, ?)', user)
    add_users_to_dictionary()

def get_users_from_db():
    with db.connect('kittybot_db.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM users')
        result = cur.fetchall()
        return result

def add_users_to_dictionary():
    users = get_users_from_db()
    if len(users):
        for user in users:
            if user[0] not in USERS:
                USERS[user[0]] = {
                    'weather': False,
                }

def update_db(user):
    with db.connect('kittybot_db.db') as con:
        cur = con.cursor()
        sql_update_query = (
            """Update users SET name = ?, last_name = ? WHERE chat_id = ?"""
        )
        data = (user[1], user[2], user[0])
        cur.execute(sql_update_query, data)
