from telegram.ext import UpdateFilter

from constants import USERS
from utils import get_chat_id


class WeatherFilter(UpdateFilter):
    def filter(self, update):
        return USERS.get(get_chat_id(update))['weather']