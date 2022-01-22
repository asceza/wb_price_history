
# https://www.crummy.com/software/BeautifulSoup/bs4/doc.ru/bs4ru.html#id28
# https://overcoder.net/q/1134944/%D0%BA%D0%B0%D0%BA-%D1%83%D0%B4%D0%B0%D0%BB%D0%B8%D1%82%D1%8C-%D1%8D%D1%82%D0%BE%D1%82-xa0-%D0%B8%D0%B7-%D1%81%D1%82%D1%80%D0%BE%D0%BA%D0%B8-%D0%B2-python


import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime
import csv


url = "https://www.wildberries.ru/catalog/42782921/detail.aspx"
id = url.split("/")[-2]
output_file = f"{id}.csv"
url_price_history = f"https://wbx-content-v2.wbstatic.net/price-history/{id}.json"
current_date = "{:%d.%m.%Y}".format(datetime.now())


def get_title_and_current_price(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    title = soup.title.text
    current_price = soup.find(class_="price-block__final-price").text.strip().replace(u'\xa0', u'').replace('₽', '')
    return title, current_price


def get_price_history(url_price_history):
    r = requests.get(url_price_history).json()
    date_row = []
    price_row = []
    for i in r:
        date = datetime.fromtimestamp(i['dt'])
        date = date.strftime('%d.%m.%Y')
        date_row.append(date)
        price_row.append(float((i['price']['RUB']) / 100))
    date_row.append(current_date)
    price_row.append(float(current_price))
    return date_row, price_row


def add_data_to_csv(row):
    with open(output_file, "a", encoding='utf-8') as file:
        writer = csv.writer(file, delimiter=';')  # вызываем метод, в параметры которого передаем наш файл
        writer.writerow(row)


if __name__ == '__main__':
    title, current_price = get_title_and_current_price(url)
    header_row = [title, url]

    date_row, price_row = get_price_history(url_price_history)

    add_data_to_csv(header_row)
    add_data_to_csv(date_row)
    add_data_to_csv(price_row)
    add_data_to_csv([])
