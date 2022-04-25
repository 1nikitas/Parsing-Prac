from bs4 import BeautifulSoup
import datetime
import requests
from fake_useragent import UserAgent
import csv
import io


def collect_data(city_code):
    cur_time = datetime.datetime.now().strftime("%d_%m_%Y_%H_%M")

    ua = UserAgent()

    headers = {
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        'User-Agent' : ua.random
    }

    cookies = {
        'mg_geo_id': f'{city_code}'
    }

    responce = requests.get(url = 'https://magnit.ru/promo/', headers=headers, cookies=cookies)
    #
    # with open('index.html', 'w') as file:
    #     file.write(response.text)


    # with open('index.html') as file:
    #     src = file.read()

    soup = BeautifulSoup(responce.text, 'lxml')

    # parsing city
    city = soup.find("a", class_ = "header__contacts-link").text.strip()
    # print(city)

    # excel file loading
    with io.open(f'{city}_{cur_time}.csv', 'w', encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow(
            (
                "Продукт",
                "Старая цена",
                "Новая цена",
                "Процент скидки",
                "Время скидки"
            )
        )


    #parsing cards with discounts
    cards = soup.find_all("a", class_ = "card-sale")

    for card in cards:
        try:
            card_discount = card.find("div", class_="card-sale__discount").text.strip()
        except:
            continue
        old_price1 = card.find("div", class_="label__price_old").find("span",
                                                                      class_="label__price-integer").text.strip()
        old_price2 = card.find("div", class_="label__price_old").find("span",
                                                                      class_="label__price-decimal").text.strip()

        old_price = f'{old_price1}.{old_price2}'

        new_price1 = card.find("div", class_="label__price_new").find("span", class_="label__price-integer").text.strip()
        new_price2 = card.find("div", class_="label__price_new").find("span", class_="label__price-decimal").text.strip()

        new_price = f'{new_price1}.{new_price2}'

        title = card.find("div", class_="card-sale__title").text.strip()
        date = card.find("div", class_="card-sale__date").text.replace("\n", ' ').strip()

        with io.open(f'{city}_{cur_time}.csv', "a", encoding="utf-8") as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    title,
                    old_price,
                    new_price,
                    card_discount,
                    date

                )
        )

    print(f"Файл {city}_{cur_time}.csv успешно записан!")




def main():

    collect_data(city_code = '2398')

if __name__ == '__main__':
    main()
