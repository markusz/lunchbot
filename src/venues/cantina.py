from datetime import datetime
# import urllib2
from bs4 import BeautifulSoup
import re

import requests

from src.models.dish import Dish


def get_lunch_for_date(date=datetime.now(), show_only_current_day=True):
    dishes = []

    res = requests.get(
        'https://wohin-essen.de/restaurantliste/restaurant/cantina.html',
        headers={'User-agent': 'crawler'}
    )
    # page = urllib2.urlopen(quote_page)
    print()
    soup = BeautifulSoup(res.content, 'html.parser')


    menu = soup.find('div', attrs={'class': 'tx_in2wm_show_all_menu_day today'})
    print(menu.text)

    splitted = menu.text.split('\n')
    filtered_content = [re.sub('\s{2,}', ' ', x.strip()) for x in splitted if len(x.strip()) > 5 and '€' in x]

    for meal in filtered_content:
        meal_desc = meal.split(' € ')[0]
        price = meal.split(' € ')[1]
        split = meal_desc.split(' mit ')

        meal_name = split[0]
        meal_ingredients = split[1] if len(split) > 1 else None
        dishes.append(Dish('Cantina', meal_name, meal_ingredients if len(splitted) > 1 else None, float(price), None))

    print(filtered_content)

    return dishes