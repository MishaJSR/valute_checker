from datetime import datetime

import requests
import xml.etree.ElementTree as ET

from redis_manager.RedisManager import RedisManager


def update_info(url):
    formatted_date = datetime.now().strftime("%d/%m/%Y")
    response = requests.get(url + formatted_date, timeout=3)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        currency_dict = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            value = round(float(valute.find('VunitRate').text.replace(",", ".")), 4)
            RedisManager.send_to_redis(key=char_code, value=value)
            currency_dict[char_code] = value
        RedisManager.send_to_redis(key="RUB", value=1)
        currency_dict["RUB"] = 1
        print(currency_dict)
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
