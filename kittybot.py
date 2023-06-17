import logging
import os
import requests

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, Filters, MessageHandler, Updater, UpdateFilter
)

from constants import USERS, URL_CAT, URL_DOG, URL_WEATHER
from utils import (
    add_user_to_db,
    add_users_to_dictionary,
    create_db,
    get_chat_id,
    get_username, restricted_access
)

create_db()
add_users_to_dictionary()
load_dotenv()
secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class WeatherFilter(UpdateFilter):
    def filter(self, update):
        return USERS.get(get_chat_id(update))['weather']

weatherfilter = WeatherFilter()

# @restricted_access  # убрать комментарий для ограничения доступа
def instructions(update, context):
    chat_id = get_chat_id(update)
    name = get_username(update)
    context.bot.send_message(
        chat_id=chat_id,
        text=(
        f'{name} я пока не умею поддерживать беседу, '
        f'выберите, пожалуйста, 1 из опций в главном меню.'
        ),
    )

# @restricted_access  # убрать комментарий для ограничения доступа
def to_main_menu(update, context):
    chat_id = get_chat_id(update)
    for value in USERS.get(chat_id):
        if USERS[chat_id][value]:
            USERS[chat_id][value] = False
    context.bot.send_message(
        chat_id=chat_id,
        text='Возвращение в главное меню',
    )

# @restricted_access  # убрать комментарий для ограничения доступа
def weather(update, context):
    chat_id = get_chat_id(update)
    USERS[chat_id]['weather'] = True
    context.bot.send_message(
        chat_id=chat_id,
        text='напечатайте название города',
    )

# @restricted_access  # убрать комментарий для ограничения доступа
def get_weather(update, context):
    chat_id = get_chat_id(update)
    msg = update.message.text
    params = {
        'format': 2,
        'M': ''
    }
    try:
        responce = requests.get(f'{URL_WEATHER}{msg}', params)
        if responce.status_code == 200:
            context.bot.send_message(
            chat_id=chat_id,
            text=responce.text,
            )
        elif responce.status_code == 404:
            context.bot.send_message(
            chat_id=chat_id,
            text='Город не найден, проверьте правильность ввода',
            )
    except Exception as error:
        logging.error(f'Ошибка при запросе к серверу погоды: {error}')
        context.bot.send_message(
            chat_id=chat_id,
            text='Ошибка на сервере погоды, попробуйте сделать запрос позже',
            )
    finally:
        to_main_menu(update, context)

# @restricted_access  # убрать комментарий для ограничения доступа
def wake_up(update, context):
    chat_id = get_chat_id(update)
    name = get_username(update)
    user = (chat_id, name)
    add_user_to_db(user)
    buttons = ReplyKeyboardMarkup(
    [['/weather'], ['/new_cat'], ['/new_dog']], resize_keyboard=True
)
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {name}, выберите, пожалуйста, одну из опций',
        reply_markup=buttons
    )

def get_new_image_cat():
    try:
        response = requests.get(URL_CAT)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = URL_DOG
        response = requests.get(new_url)
    response = response.json()
    random_cat = response[0].get('url')
    return random_cat

def get_new_image_dog():
    try:
        response = requests.get(URL_DOG)
    except Exception as error:
        logging.error(f'Ошибка при запросе к основному API: {error}')
        new_url = URL_CAT
        response = requests.get(new_url)
    response = response.json()
    random_dog = response[0].get('url')
    return random_dog

# @restricted_access  # убрать комментарий для ограничения доступа
def new_cat(update, context):
    chat_id = get_chat_id(update)
    context.bot.send_photo(chat_id, get_new_image_cat())

# @restricted_access  # убрать комментарий для ограничения доступа
def new_dog(update, context):
    chat_id = get_chat_id(update)
    context.bot.send_photo(chat_id, get_new_image_dog())

def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.dispatcher.add_handler(CommandHandler('new_cat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('new_dog', new_dog))
    updater.dispatcher.add_handler(MessageHandler(weatherfilter, get_weather))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, instructions))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
