import requests

from datetime import datetime
from date_util import to_date
from dish import Dish

MAIN = 4

def food_menu_applies_today(provider):
    return to_date(provider['speiseplanAdvanced']['gueltigVon']) <= datetime.today().date() <= to_date(
        provider['speiseplanAdvanced']['gueltigBis'])

def get_cantine_lunch():
    res = requests.get(
        'http://leonardi.webspeiseplan.de/index.php?token=d38436e0839755e6cde59cbda0fff016&model=menu&location=2100&languagetype=1&_=1513876707612',
        headers={'User-agent': 'crawler'}
    )

    dishes = []
    date_string = datetime.now().strftime('%Y-%m-%d')
    date_string = '2017-12-28'

    for food_offer in res.json()['content']:
        if food_offer['speiseplanAdvanced']['anzeigename'].strip() == 'Speisenkarte Essbar':
            for menu_item in (food_offer['speiseplanGerichtData']):
                dish = menu_item['speiseplanAdvancedGericht']
                if (dish['datum'].startswith(date_string) and dish['gerichtkategorieID'] == MAIN):
                    venue_name = food_offer['speiseplanAdvanced']['anzeigename'].strip()
                    full_dish = dish['gerichtname'].strip().split(' I ', 1)
                    dish_name = full_dish[0].strip().replace(' I', ',')
                    ingredients = full_dish[1].strip().replace(' I', ',') if len(full_dish) > 1 else ''
                    price = menu_item['zusatzinformationen'].get('mitarbeiterpreisDecimal2', None)
                    kcal = menu_item['zusatzinformationen'].get('nwkcalInteger', None)

                    dishes.append(Dish('Kantine', dish_name, ingredients, price, kcal))

    return dishes