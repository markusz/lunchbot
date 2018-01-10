from datetime import datetime

import requests

from src.utils.date_util import to_date
from src.models.dish import Dish

MAIN = 4


def food_menu_applies_today(provider):
    return to_date(provider['speiseplanAdvanced']['gueltigVon']) <= datetime.today().date() <= to_date(
        provider['speiseplanAdvanced']['gueltigBis'])


def get_cantine_lunch(date=datetime.now()):
    res = requests.get(
        'http://leonardi.webspeiseplan.de/index.php?token=d38436e0839755e6cde59cbda0fff016&model=menu&location=2100&languagetype=1&_=1513876707612',
        headers={'User-agent': 'crawler'}
    )

    dishes = []
    date_string = date.strftime('%Y-%m-%d')
    # date_string = '2017-12-28'

    for food_offer in res.json()['content']:
        if food_offer['speiseplanAdvanced']['anzeigename'].strip() == 'Speisenkarte Essbar':
            for menu_item in (food_offer['speiseplanGerichtData']):
                dish = menu_item['speiseplanAdvancedGericht']
                if dish['datum'].startswith(date_string) and dish['gerichtkategorieID'] == MAIN:
                    full_dish = dish['gerichtname'].strip().split(' I ', 1)
                    dish_name = full_dish[0].strip().replace(' I', ',')
                    ingredients = full_dish[1].strip().replace(' I', ',') if len(full_dish) > 1 else ''
                    price = menu_item['zusatzinformationen'].get('mitarbeiterpreisDecimal2', None)
                    kcal = menu_item['zusatzinformationen'].get('nwkcalInteger', None)
                    kj = menu_item['zusatzinformationen'].get('nwkjInteger', None)

                    # API sometimes mislabels kj and kcal leading to unrealistic kcal values
                    actual_kcal = min(kcal, kj)

                    dishes.append(Dish('Kantine', dish_name, ingredients, price, actual_kcal))

    return dishes
