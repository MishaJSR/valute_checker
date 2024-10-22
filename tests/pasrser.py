from datetime import datetime

import requests
import xml.etree.ElementTree as ET


# url = "https://cbr.ru/scripts/XML_daily.asp?date_req=20/03/2024"

def update_info(url):
    formatted_date = datetime.now().strftime("%d/%m/%Y")
    response = requests.get(url + formatted_date, timeout=3)

    if response.status_code == 200:
        root = ET.fromstring(response.content)
        currency_dict = {}
        for valute in root.findall('Valute'):
            char_code = valute.find('CharCode').text
            value = round(float(valute.find('VunitRate').text.replace(",", ".")), 4)
            currency_dict[char_code] = value
        print(currency_dict)
    else:
        print(f"Ошибка при выполнении запроса: {response.status_code}")
