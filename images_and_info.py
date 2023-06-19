from http import HTTPStatus
import logging

from bs4 import BeautifulSoup
import requests

from constants import CAT_URL, DOG_URL, HOROSCOPE_URL, WEATHER_URL


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

horoscope_signs_links = {
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


def horoscope_sign_info(sign):
    failed = 'Ошибка на сервере гороскопа, попробуйте сделать запрос позже'
    sign = sign.lower()
    if sign not in horoscope_signs_links:
        return 'Такого знака зодиака не существует!'
    link = horoscope_signs_links.get(sign)
    try:
        response = requests.get(link)
        if response.status_code != HTTPStatus.OK:
            logging.error(
                f'Статус код != 200 ,'
                f'полученный статус код: {response.status_code}'
            )
            return failed
    except Exception as error:
        logging.error(f'Ошибка при запросе к сайту гороскопа: {error}')
        return failed
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find('p').text.strip('<p>')


def weather_info(city):
    failed = 'Ошибка на сервере погоды, попробуйте сделать запрос позже'
    params = {
        'format': 2,
        'M': ''
    }
    result = None
    try:
        response = requests.get(f'{WEATHER_URL}{city}', params)
        if response.status_code == HTTPStatus.OK:
            result = response.text
        elif response.status_code == HTTPStatus.NOT_FOUND:
            result = 'Город не найден'
        else:
            result = failed
    except Exception as error:
        logging.error(f'Ошибка при запросе к API погоды: {error}')
        result = failed
    return result


def get_new_image_cat():
    try:
        response = requests.get(CAT_URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к cat_API: {error}')
        new_url = DOG_URL
        response = requests.get(new_url)
    response = response.json()
    result = response[0].get('url')
    return result


def get_new_image_dog():
    try:
        response = requests.get(DOG_URL)
    except Exception as error:
        logging.error(f'Ошибка при запросе к dog_API: {error}')
        new_url = CAT_URL
        response = requests.get(new_url)
    response = response.json()
    result = response[0].get('url')
    return result
