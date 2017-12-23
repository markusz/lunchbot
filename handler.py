import json
from tabulate import tabulate
from hacker_handler import get_hacker_lunch
from leonardi_handler import get_cantine_lunch

def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    all_dishes = []

    leonardi_results = get_cantine_lunch()
    hacker_results = get_hacker_lunch()

    all_dishes.extend(leonardi_results)
    all_dishes.extend(hacker_results)
    print(json.dumps(all_dishes, default=lambda o: o.__dict__))

    squared = list(map(lambda x: x.to_array(), all_dishes))
    print(tabulate(squared))
    return response

if __name__ == '__main__':
    res = hello(123, None)
