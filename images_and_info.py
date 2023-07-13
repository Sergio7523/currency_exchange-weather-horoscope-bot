from http import HTTPStatus
import logging

from bs4 import BeautifulSoup
import requests

from constants import (
    CAT_URL,
    CURRENCIES,
    CURRENCIES_URL,
    DOG_URL,
    HOROSCOPE_SIGNS,
    HOROSCOPE_URL,
    WEATHER_URL
)


logging.basicConfig(
    format=(
        '%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s'
    ),
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    encoding='utf-8'
)


def horoscope_sign_info(msg):
    failed = 'Ошибка на сервере гороскопа, попробуйте сделать запрос позже'
    incorrect_request = 'Некорректный запрос'
    msg = msg.lower().split()
    if len(msg) not in (1, 2):
        return incorrect_request
    if len(msg) == 2 and msg[0] in HOROSCOPE_SIGNS and msg[1] == 'неделя':
        sign, _ = msg
        params = {
            'znak': HOROSCOPE_SIGNS.get(sign),
            'kn': 'week'
        }
    elif len(msg) == 1 and msg[0] in HOROSCOPE_SIGNS:
        sign = msg[0]
        params = {
            'znak': HOROSCOPE_SIGNS.get(sign)
        }
    else:
        return incorrect_request
    url = HOROSCOPE_URL
    try:
        response = requests.get(url, params=params)
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
    return (
        soup.find('p').text.strip('<p>') if len(msg) == 1
        else '\n ** '.join(
            [
                day_info.get_text().strip('<p>')
                for day_info in soup.find_all('p')
            ]
        )
    )


def weather_info(city):
    failed = 'Ошибка на сервере погоды, попробуйте сделать запрос позже'
    params = {
        'format': 4,
        'M': '',
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


def currency_info(requested_values):
    message = 'Некорректный запрос'
    requested_values = requested_values.lower().split()
    if len(requested_values) != 3:
        return message
    amount, currency_from, currency_to = requested_values
    if currency_from not in CURRENCIES or currency_to not in CURRENCIES:
        return message
    try:
        amount = float(amount)
    except ValueError:
        return message
    url = f'{CURRENCIES_URL}/{currency_from}/{currency_to}'
    try:
        response = requests.get(url)
    except Exception as error:
        logging.error(f'Ошибка при запросе к API валют: {error}')
        message = 'Ошибка на сервере курсов валют'
    currency_rate = response.json()
    result = amount * currency_rate
    message = (
        f'{amount:.2f} {CURRENCIES.get(currency_from)} '
        f'= {result:.2f} {CURRENCIES.get(currency_to)}'
    )
    return message
