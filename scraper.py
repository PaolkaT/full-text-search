import json
import os
import re

import requests
from bs4 import BeautifulSoup

filename = 'bashim.json'
# основной url, список всех рецептов
url = 'https://bash.im/index/'

# id для нумерации всех цитат
id = 0


def parse_quote(text):
    new_text = text
    while '<br>' in new_text:
        new_text = new_text.replace('<br>', '')
    new_text = new_text.replace('Комикс по мотивам цитаты', '')
    new_text = new_text.replace('Комиксы по мотивам цитаты', '')
    new_text = re.sub('  +', '', new_text)
    new_text = re.sub('\n\n+', '', new_text)
    return new_text


def parse_date(text):
    new_text = text.replace(' ', '')
    return new_text[1:11]


pages = 3434

with open(filename, 'a', encoding='utf-8') as f:
    f.write('[')
    for page_number in range(1, pages + 1):
        url_local = f'{url}{page_number}'
        html_text = requests.get(url_local).text
        soup = BeautifulSoup(html_text, 'lxml')

        quotes = soup.find_all('article', class_='quote')
        for i in range(len(quotes)):
            quote = quotes[i]
            id += 1
            quotes_dict = {}
            # основные данные
            id_im = quote.find('a', class_='quote__header_permalink').text

            rating = quote.find('div', class_='quote__total').text

            date = parse_date(quote.find('div', class_='quote__header_date').text)

            quote_text = parse_quote(quote.find('div', class_="quote__body").text)
            # заполнение словаря данными
            quotes_dict['id'] = id
            quotes_dict['quote_id'] = id_im
            quotes_dict['rating'] = rating
            quotes_dict['date'] = date
            quotes_dict['quote_text'] = quote_text
            json.dump(quotes_dict, f, ensure_ascii=False)
            f.write(',\n')
with open(filename, 'rb+') as f:
    f.seek(-3, os.SEEK_END)
    f.truncate()
with open(filename, 'a', encoding='utf-8') as f:
    f.write(']')
