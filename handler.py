import json
import re
from datetime import datetime

from tabulate import tabulate

from src.venues.cantina import get_lunch_for_date as cantina_scrape
from src.venues.hacker import get_lunch_for_date as hacker_scrape
from src.venues.leonardi import get_lunch_for_date as leonardi_scrape
from src.venues.mace import get_lunch_for_date as mace_scrape
from src.venues.schroeders import get_lunch_for_date as schroeders_scrape


def filter(filters, dish, inclusive):
    if len(filters) < 1:
        return inclusive

    for filter in filters:
        if re.search(filter, dish.venue, re.IGNORECASE):
            return True

    return False


def get_all_dishes(event, context):
    print(event)

    max_kcal = 10000000  # python 3 does not have max int
    max_price = 10000000
    as_json = False
    only = []
    exclude = []
    query_strings = event.get('queryStringParameters')

    if query_strings is not None:
        max_kcal = int(query_strings.get('maxkcal', max_kcal))
        max_price = float(query_strings.get('maxprice', max_price))
        as_json = bool(query_strings.get('json', False))

        exclude_query_string = query_strings.get('exclude')
        only_query_string = query_strings.get('only')

        only = only_query_string.split(',') if type(only_query_string) is str else []
        exclude = exclude_query_string.split(',') if type(exclude_query_string) is str else []

    all_dishes = []

    date = datetime.now()

    all_dishes.extend(leonardi_scrape(date))
    all_dishes.extend(hacker_scrape(date))
    all_dishes.extend(cantina_scrape(date))
    all_dishes.extend(mace_scrape(date))
    all_dishes.extend(schroeders_scrape(date))

    filtered_dishes = [
        dish
        for dish
        in all_dishes
        if
        dish.cheapter_than(max_price)
        and dish.less_kcal_than(max_kcal)
        and filter(only, dish, True)
        and not filter(exclude, dish, False)
    ]

    result_json = json.dumps(filtered_dishes, default=lambda o: o.__dict__)
    text_array = list(map(lambda x: x.to_array(), filtered_dishes))

    response_body = result_json if as_json else tabulate(text_array)
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
            "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
        },
        "body": response_body
    }

    print(response_body)
    return response


if __name__ == '__main__':
    event = {'queryStringParameters':
        {
            # 'json': 'true',
            # 'only': 'mace,hacker',
            # 'maxkcal': 1000,
            # 'maxprice': 5.00
        }
    }
    res = get_all_dishes(event, None)
    # schroeders_scrape()
