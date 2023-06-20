import os

from dotenv import load_dotenv


load_dotenv()

WEATHER_URL = 'http://wttr.in/'
CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'
HOROSCOPE_URL = 'https://1001goroskop.ru/?znak='
CURRENCIES_URL = 'https://api.coingate.com/v2/rates/merchant/'

HOROSCOPE_SIGNS_URLS = {
    'овен': f'{HOROSCOPE_URL}aries',
    'телец': f'{HOROSCOPE_URL}taurus',
    'близнецы': f'{HOROSCOPE_URL}gemini',
    'рак': f'{HOROSCOPE_URL}cancer',
    'лев': f'{HOROSCOPE_URL}leo',
    'дева': f'{HOROSCOPE_URL}virgo',
    'весы': f'{HOROSCOPE_URL}libra',
    'скорпион': f'{HOROSCOPE_URL}scorpio',
    'стрелец': f'{HOROSCOPE_URL}sagittarius',
    'козерог': f'{HOROSCOPE_URL}capricorn',
    'водолей': f'{HOROSCOPE_URL}aquarius',
    'рыбы': f'{HOROSCOPE_URL}pisces',
}

USERS = {}
ALLOWED_USERS = os.getenv('ALLOWED_USERS').split(',')

CURRENCIES = ('rub', 'usd', 'eur')
