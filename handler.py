import json
from datetime import datetime

from tabulate import tabulate

from src.venues.hacker import get_hacker_lunch
from src.venues.leonardi import get_cantine_lunch


def get_all_dishes(event, context):
    print(event)

    all_dishes = []

    date = datetime.now()
    print(date)

    leonardi_results = get_cantine_lunch(date)
    hacker_results = get_hacker_lunch(date)

    all_dishes.extend(leonardi_results)
    all_dishes.extend(hacker_results)
    result_json = json.dumps(all_dishes, default=lambda o: o.__dict__)

    # print(result_json)

    squared = list(map(lambda x: x.to_array(), all_dishes))
    print(tabulate(squared))

    response = {
        "statusCode": 200,
        "body": result_json
    }
    return response


if __name__ == '__main__':
    res = get_all_dishes(123, None)
