import os

from dotenv import load_dotenv


load_dotenv()

URL_WEATHER = 'http://wttr.in/'
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'

USERS = {}
ALLOWED_USERS = os.getenv('ALLOWED_USERS').split(',')
