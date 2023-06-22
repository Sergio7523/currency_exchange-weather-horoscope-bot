from telegram.ext import UpdateFilter

from utils import (
    get_chat_id, get_user_currency, get_user_horoscope, get_user_weather
)


class WeatherFilter(UpdateFilter):
    def filter(self, update):
        return get_user_weather(get_chat_id(update))


class HoroscopeFilter(UpdateFilter):
    def filter(self, update):
        return get_user_horoscope(get_chat_id(update))


class CurrencyFilter(UpdateFilter):
    def filter(self, update):
        return get_user_currency(get_chat_id(update))
