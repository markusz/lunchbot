import json
from datetime import datetime
from functools import reduce

from tabulate import tabulate

import src.venues.cantina as cantina
import src.venues.hacker as hacker
import src.venues.leonardi as leonardi
import src.venues.mace as mace
import src.venues.schroeders as schroeders
from src.utils.filter_util import filter_dishes_by_user_filters, query_to_filter_params

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",  # Required for CORS support to work
    "Access-Control-Allow-Credentials": True  # Required for cookies, authorization headers with HTTPS
}


def serve_html(event, context):
    import codecs
    html = codecs.open("./web/index.html", 'r')

    response = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/html',
        },
        'body': html.read()
    }

    return response


def get_all_dishes(event, context):
    print(event)
    date = datetime.now()

    all_dishes = get_all_dishes_for_date(date)

    filters = query_to_filter_params(event.get('queryStringParameters'))

    filtered_dishes = filter_dishes_by_user_filters(all_dishes, filters)
    response_body = dishes_to_proper_response_format(filtered_dishes, filters)

    print(response_body)
    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": response_body
    }


def get_all_dishes_for_date(date):
    # flatmap
    return reduce(list.__add__, [
        leonardi.get_lunch_for_date(date),
        hacker.get_lunch_for_date(date),
        cantina.get_lunch_for_date(date),
        mace.get_lunch_for_date(date),
        schroeders.get_lunch_for_date(date)
    ])


def dishes_to_proper_response_format(dishes, filters):
    if filters.get('as_json'):
        return json.dumps(dishes, default=lambda o: o.__dict__)

    text_array = list(map(lambda x: x.to_array(), dishes))
    return tabulate(text_array)


if __name__ == '__main__':
    event = {
        'queryStringParameters':
        {
            'json': 'false',
            # 'only': 'mace,hacker',
            # 'maxkcal': 1000,
            # 'maxprice': 5.00
        }
    }
    res = get_all_dishes(event, None)
