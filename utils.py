import os

from dotenv import load_dotenv

load_dotenv()

USERS = {}
ALLOWED_USERS = os.getenv('ALLOWED_USERS').split(',')


def get_chat_id(update):
    chat_id = str(update.effective_chat.id)
    return chat_id

def add_user(func):
    def wrapper(*args, **kwargs):
        chat_id = get_chat_id(args[0])
        if chat_id not in USERS:
            USERS[chat_id] = {
                'weather': False,
                'username': args[0].message.chat.username
            }
        return func(*args, **kwargs)
    return wrapper
