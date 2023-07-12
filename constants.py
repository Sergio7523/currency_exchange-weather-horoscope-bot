import os

from dotenv import load_dotenv


load_dotenv()

WEATHER_URL = 'http://wttr.in/'
CAT_URL = 'https://api.thecatapi.com/v1/images/search'
DOG_URL = 'https://api.thedogapi.com/v1/images/search'
HOROSCOPE_URL = 'https://1001goroskop.ru/'
CURRENCIES_URL = 'https://api.coingate.com/v2/rates/merchant/'

HOROSCOPE_SIGNS = {
    'овен': 'aries',
    'телец': 'taurus',
    'близнецы': 'gemini',
    'рак': 'cancer',
    'лев': 'leo',
    'дева': 'virgo',
    'весы': 'libra',
    'скорпион': 'scorpio',
    'стрелец': 'sagittarius',
    'козерог': 'capricorn',
    'водолей': 'aquarius',
    'рыбы': 'pisces',
}

ALLOWED_USERS = os.getenv('ALLOWED_USERS').split(', ')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
BOT_OWNER = os.getenv('BOT_OWNER')

CURRENCIES = {
    'rub': 'Russian Ruble',
    'usd': 'United States Dollar',
    'eur': 'Euro',
    'gbp': 'British Pound',
    'pln': 'Polish Zloty',
    'czk': 'Czech Republic Koruna',
    'sek': 'Swedish Krona',
    'nok': 'Norwegian Krone',
    'dkk': 'Danish Krone',
    'chf': 'Swiss Franc',
    'zar': 'South African Rand',
    'aud': 'Australian Dollar',
    'jpy': 'Japanese Yen',
    'nzd': 'New Zealand Dollar',
    'try': 'Turkish Lira',
    'brl': 'Brazilian Real',
    'cad': 'Canadian Dollar',
    'cny': 'Chinese Yuan Renminbi',
    'hkd': 'Hong Kong Dollar',
    'huf': 'Hungarian Forint',
    'inr': 'Indian Rupee',
    'ils': 'Israeli New Shekel',
    'myr': 'Malaysian Ringgit',
    'mxn': 'Mexican Peso',
    'sgd': 'Singapore Dollar',
    'ron': 'Romanian Leu',
    'idr': 'Indonesian Rupiah',
    'php': 'Philippine Peso',
    'ars': 'Argentine Peso',
    'thb': 'Thai Baht',
    'ngn': 'Nigerian Naira',
    'pkr': 'Pakistani Rupee',
    'aed': 'United Arab Emirates Dirham',
    'uah': 'Ukrainian Hryvnia',
    'bgn': 'Bulgarian Lev',
    'hrk': 'Croatian Kuna',
    'rsd': 'Serbian Dinar',
    'twd': 'New Taiwan Dollar',
    'clp': 'Chilean Peso',
    'krw': 'South Korean won',
    'egp': 'Egyptian pound',
    'sar': 'Saudi riyal',
    'qar': 'Qatari riyal'
}
