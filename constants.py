import os

from dotenv import load_dotenv


load_dotenv()

WEATHER_URL = 'http://wttr.in/'
CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'
HOROSCOPE_URL = 'https://1001goroskop.ru/?znak='

USERS = {}
ALLOWED_USERS = os.getenv('ALLOWED_USERS').split(',')
