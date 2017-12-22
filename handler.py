import json
from tabulate import tabulate
from leonardi_handler import get_cantine_lunch

class MenuItem:
    """A simple example class"""
    i = 12345

    def f(self):
        return 'hello world'


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    leonardi_results = get_cantine_lunch()
    print(tabulate(leonardi_results))

    return response

if __name__ == '__main__':
    res = hello(123, None)
