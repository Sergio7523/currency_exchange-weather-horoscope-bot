import logging
import os
import requests

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, Filters, MessageHandler, Updater, UpdateFilter
)

from utils import add_user, get_chat_id, ALLOWED_USERS, USERS

load_dotenv()
secret_token = os.getenv('TOKEN')

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class WeatherFilter(UpdateFilter):
    def filter(self, update):
        if (
            USERS.get(get_chat_id(update)) is None  # временная мера, убрать при подключении бд
            or USERS.get(get_chat_id(update))['weather']
        ):
            return True


weatherfilter = WeatherFilter()
URL_WEATHER = 'http://wttr.in/'
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'

def restricted_access(func):
    def wrapper(*args, **kwargs):
        chat_id = get_chat_id(args[0])
        if chat_id in ALLOWED_USERS:
            return func(*args, **kwargs)
        else:
            args[1].bot.send_message(
                chat_id=chat_id,
                text='У Вас нет доступа к этому боту'
            )
    return wrapper

# @restricted_access  # убрать комментарий для ограничения доступа
@add_user
def instructions(update, context):
    chat_id = get_chat_id(update)
    name = update.message.chat.first_name
    context.bot.send_message(
        chat_id=chat_id,
        text=(
        f'{name} я пока не умею поддерживать беседу, '
        f'выберите, пожалуйста, 1 из опций в главном меню.'
        ),
    )
    to_main_menu(update, context)

# @restricted_access  # убрать комментарий для ограничения доступа
@add_user
def to_main_menu(update, context):
    chat_id = get_chat_id(update)
    for value in USERS.get(chat_id):
        if type(USERS[chat_id][value]) is bool and USERS[chat_id][value]:
            USERS[chat_id][value] = False
    button = ReplyKeyboardMarkup(
        [['/weather'], ['/new_cat'], ['/new_dog']], resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat_id,
        text='Возвращение в главное меню',
        reply_markup=button
    )

# @restricted_access  # убрать комментарий для ограничения доступа
@add_user
def weather(update, context):
    chat_id = get_chat_id(update)
    USERS[chat_id]['weather'] = True
    context.bot.send_message(
        chat_id=chat_id,
        text='напечатайте название города',
    )

# @restricted_access  # убрать комментарий для ограничения доступа
@add_user
def get_weather(update, context):
    chat_id = get_chat_id(update)
    msg = update.message.text
    params = {
        'format': 2,
        'M': ''
    }
    USERS[chat_id]['weather'] = False
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
    except:
        context.bot.send_message(
            chat_id=chat_id,
            text='Ошибка на сервере погоды, попробуйте сделать запрос позже',
            )
    finally:
        to_main_menu(update, context)

# @restricted_access  # убрать комментарий для ограничения доступа
@add_user
def wake_up(update, context):
    chat_id = get_chat_id(update)
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup(
        [['/weather'], ['/new_cat'], ['/new_dog']], resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {name}, выберите, пожалуйста, одну из опций',
        reply_markup=button
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
@add_user
def new_cat(update, context):
    chat_id = get_chat_id(update)
    context.bot.send_photo(chat_id, get_new_image_cat())

# @restricted_access  # убрать комментарий для ограничения доступа
@add_user
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
