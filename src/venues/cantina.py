import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.models.dish import Dish
from src.utils.text_util import extract_data_from_text

url = 'https://wohin-essen.de/restaurantliste/restaurant/cantina.html'


def get_lunch_for_date(date=datetime.now(), show_only_current_day=True):
    try:
        dishes = []

        res = requests.get(
            url,
            headers={'User-agent': 'crawler'}
        )
        soup = BeautifulSoup(res.content, 'html.parser')

        menu = soup.find('div', attrs={'class': 'tx_in2wm_show_all_menu_day today'})

        splitted = menu.text.split('\n')
        filtered_content = [re.sub('\s{2,}', ' ', x.strip()) for x in splitted if len(x.strip()) > 5 and '€' in x]

        for meal in filtered_content:
            meal_price = re.match(r'(.+?)([0-9]+,[0-9]{2}|[0-9]+.[0-9]{2})', meal)

            meal_desc = re.sub(' *€ *', '', meal_price.group(1))
            price = meal_price.group(2)
            price = re.sub(',', '.', price)

            split = extract_data_from_text(meal_desc)

            meal_name = split[0]
            meal_ingredients = split[1]
            dishes.append(Dish('Cantina', meal_name, meal_ingredients if len(splitted) > 1 else None, float(price), src=url))

        return dishes
    except Exception as err:
        print(err)
        return []
