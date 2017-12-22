import requests

from datetime import datetime
from date_util import to_date

MAIN = 4

def food_menu_applies_today(provider):
    return to_date(provider['speiseplanAdvanced']['gueltigVon']) <= datetime.today().date() <= to_date(
        provider['speiseplanAdvanced']['gueltigBis'])

def get_cantine_lunch():
    res = requests.get(
        'http://leonardi.webspeiseplan.de/index.php?token=d38436e0839755e6cde59cbda0fff016&model=menu&location=2100&languagetype=1&_=1513876707612',
        headers={'User-agent': 'crawler'}
    )

    results = []
    date_string = datetime.now().strftime('%Y-%m-%d')

    for food_offer in res.json()['content']:
        if food_offer['speiseplanAdvanced']['anzeigename'].strip() == 'Speisenkarte Essbar':
            for menu_item in (food_offer['speiseplanGerichtData']):
                dish = menu_item['speiseplanAdvancedGericht']
                if (dish['datum'].startswith('2017-12-21') and dish['gerichtkategorieID'] == MAIN):
                    venue_name = food_offer['speiseplanAdvanced']['anzeigename'].strip()
                    full_dish = dish['gerichtname'].strip().split(' I ', 1)
                    dish_name = full_dish[0].strip().replace(' I', ',')
                    ingredients = full_dish[1].strip().replace(' I', ',') if len(full_dish) > 1 else ''
                    price_dec = menu_item['zusatzinformationen'].get('mitarbeiterpreisDecimal2', None)
                    price = '%0.2f' % price_dec if price_dec != None else 'n/a'
                    kcal = str(menu_item['zusatzinformationen'].get('nwkcalInteger', 'n/a'))

                    results.append([dish_name, ingredients, price+'€', kcal])

    return results