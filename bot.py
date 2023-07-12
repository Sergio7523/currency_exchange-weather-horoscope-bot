import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, Filters, MessageHandler, Updater
)

from constants import CURRENCIES, USERS
from filters import CurrencyFilter, HoroscopeFilter, WeatherFilter
from images_and_info import (
    currency_info,
    horoscope_sign_info,
    weather_info,
    get_new_image_cat,
    get_new_image_dog
)

from utils import (
    add_user_to_db,
    add_users_to_dictionary,
    create_db,
    get_users_from_db,
    get_chat_id,
    get_username,
    reset,
    restricted_access,
    update_db
)

create_db()
add_users_to_dictionary()
load_dotenv()
secret_token = os.getenv('TOKEN')
weather_filter = WeatherFilter()
horoscope_filter = HoroscopeFilter()
currencyfilter = CurrencyFilter()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def get_buttons(chat_id):
    buttons = ReplyKeyboardMarkup(
        [
            ['/weather', '/horoscope'],
            ['/new_cat', '/new_dog'],
            ['/currency', '/user_info']
        ],
        resize_keyboard=True
    )
    if USERS[chat_id].horoscope:
        buttons = ReplyKeyboardMarkup(
            [
                ['овен', 'телец', 'близнецы'],
                ['рак', 'лев', 'дева'],
                ['весы', 'скорпион', 'стрелец'],
                ['козерог', 'водолей', 'рыбы']
            ],
            resize_keyboard=True,
        )
    return buttons


def user_info(update, context):
    chat_id = get_chat_id(update)
    name, last_name = get_username(update)
    if not last_name:
        last_name = 'фамилия не указана'
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            f'Информация вашего профиля:\n'
            f'ID чата: {chat_id}\n'
            f'имя: {name}\n'
            f'фамилия: {last_name}\n'
        ),
        reply_markup=get_buttons(chat_id)
    )
    reset(chat_id)


# @restricted_access  # убрать комментарий для ограничения доступа
def instructions(update, context):
    chat_id = get_chat_id(update)
    name, _ = get_username(update)
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            f'{name} я пока не умею поддерживать беседу, '
            f'выберите, пожалуйста, 1 из опций в главном меню.'
        ),
        reply_markup=get_buttons(chat_id)
    )


@restricted_access  # Закомментировать для снятия ограничения
def weather(update, context):
    chat_id = get_chat_id(update)
    USERS[chat_id].weather = True
    context.bot.send_message(
        chat_id=chat_id,
        text='напечатайте название города',
    )


def get_weather(update, context):
    chat_id = get_chat_id(update)
    city = update.message.text
    reset(chat_id)
    result = weather_info(city)
    context.bot.send_message(
        chat_id=chat_id,
        text=result,
        reply_markup=get_buttons(chat_id)
    )


@restricted_access  # Закомментировать для снятия ограничения
def horoscope(update, context):
    chat_id = get_chat_id(update)
    USERS[chat_id].horoscope = True
    context.bot.send_message(
        chat_id=chat_id,
        text='выберите знак зодиака',
        reply_markup=get_buttons(chat_id)
    )


def get_horoscope(update, context):
    chat_id = get_chat_id(update)
    message = update.message.text
    reset(chat_id)
    result = horoscope_sign_info(message)
    context.bot.send_message(
        chat_id=chat_id,
        text=result,
        reply_markup=get_buttons(chat_id)
    )


@restricted_access  # Закомментировать для снятия ограничения
def currency(update, context):
    chat_id = get_chat_id(update)
    USERS[chat_id].currency = True
    context.bot.send_message(
        chat_id=chat_id,
        text=(
            f'Введите количество валюты и любую валютную пару\n'
            f'например: 1000 rub eur или 10.90 (10 долларов 90 центов) '
            f'usd msn\n'
            f'коды поддерживаемых валют:\n'
            f'{", ".join(value for value in CURRENCIES)}'
        )
    )


def get_currency(update, context):
    chat_id = get_chat_id(update)
    requested_values = update.message.text
    reset(chat_id)
    result = currency_info(requested_values)
    context.bot.send_message(
        chat_id=chat_id,
        text=result,
        reply_markup=get_buttons(chat_id)
    )


# @restricted_access  # убрать комментарий для ограничения доступа
def wake_up(update, context):
    chat_id = get_chat_id(update)
    name, last_name = get_username(update)
    user = (chat_id, name, last_name)
    users_in_db = get_users_from_db()
    chat_ids_in_db = [user_chat_id[0] for user_chat_id in users_in_db]
    if chat_id not in chat_ids_in_db:
        add_user_to_db(user)
    elif chat_id in chat_ids_in_db and user not in users_in_db:
        update_db(user)
    context.bot.send_message(
        chat_id=chat_id,
        text=f'Привет, {name}, выберите, пожалуйста, одну из опций',
        reply_markup=get_buttons(chat_id)
    )


@restricted_access  # Закомментировать для снятия ограничения
def new_cat(update, context):
    chat_id = get_chat_id(update)
    context.bot.send_photo(chat_id, get_new_image_cat())
    reset(chat_id)


@restricted_access  # Закомментировать для снятия ограничения
def new_dog(update, context):
    chat_id = get_chat_id(update)
    context.bot.send_photo(chat_id, get_new_image_dog())
    reset(chat_id)


def main():
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('weather', weather))
    updater.dispatcher.add_handler(CommandHandler('horoscope', horoscope))
    updater.dispatcher.add_handler(CommandHandler('currency', currency))
    updater.dispatcher.add_handler(CommandHandler('new_cat', new_cat))
    updater.dispatcher.add_handler(CommandHandler('new_dog', new_dog))
    updater.dispatcher.add_handler(CommandHandler('user_info', user_info))
    updater.dispatcher.add_handler(MessageHandler(weather_filter, get_weather))
    updater.dispatcher.add_handler(
        MessageHandler(horoscope_filter, get_horoscope)
    )
    updater.dispatcher.add_handler(
        MessageHandler(currencyfilter, get_currency)
    )
    updater.dispatcher.add_handler(MessageHandler(Filters.text, instructions))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
