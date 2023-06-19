from http import HTTPStatus

from bs4 import BeautifulSoup
import requests

from constants import CAT_URL, DOG_URL, HOROSCOPE_URL, WEATHER_URL

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
    link = horoscope_signs_links.get(sign)
    response = requests.get(link)
    if response.status_code != HTTPStatus.OK:
        return 'Ошибка на сервере гороскопа, попробуйте сделать запрос позже'
    soup = BeautifulSoup(response.text, "html.parser")
    return soup.find('p').text.strip('<p>')


def weather_info(city):
    params = {
        'format': 2,
        'M': ''
    }
    response = requests.get(f'{WEATHER_URL}{city}', params)
    result = None
    if response.status_code == HTTPStatus.OK:
        result = response.text
    elif response.status_code == HTTPStatus.NOT_FOUND:
        result = 'Город не найден'
    else:
        result = 'Ошибка на сервере погоды, попробуйте сделать запрос позже'
    return result


def get_new_image_cat():
    response = requests.get(CAT_URL)
    if response.status_code != HTTPStatus.OK:
        new_url = DOG_URL
        response = requests.get(new_url)
    response = response.json()
    result = response[0].get('url')
    return result


def get_new_image_dog():
    response = requests.get(DOG_URL)
    if response.status_code != HTTPStatus.OK:
        new_url = CAT_URL
        response = requests.get(new_url)
    response = response.json()
    result = response[0].get('url')
    return result
