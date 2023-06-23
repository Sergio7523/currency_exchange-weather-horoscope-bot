from telegram.ext import UpdateFilter

from utils import (
    get_chat_id, get_user_statuses
)


class WeatherFilter(UpdateFilter):
    def filter(self, update):
        return get_user_statuses(get_chat_id(update))[0]


class HoroscopeFilter(UpdateFilter):
    def filter(self, update):
        return get_user_statuses(get_chat_id(update))[1]


class CurrencyFilter(UpdateFilter):
    def filter(self, update):
        return get_user_statuses(get_chat_id(update))[2]
