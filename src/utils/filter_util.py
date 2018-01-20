import re

A_VERY_HIGH_NUMBER = 100000000000


def extract_data_from_text(text):
    text = re.sub(r' {2,}', ' ', text)
    m = re.match(r'((.+?) (mit|-|auf) ?(.+)?|(.+))', text)

    if m.group(2) is not None:
        result = (m.group(2), m.group(4))
    else:
        result = (m.group(1), None)

    return result


def filter_dishes(filters, dish, inclusive):
    if len(filters) < 1:
        return inclusive

    for filter in filters:
        if re.search(filter, dish.venue, re.IGNORECASE):
            return True

    return False


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def query_to_filter_params(query_strings):
    default_filter =   {
        'max_kcal': A_VERY_HIGH_NUMBER,
        'max_price': A_VERY_HIGH_NUMBER,
        'as_json': True,
        'only': [],
        'exclude': []
    }

    if query_strings is not None:
        exclude_query_string = query_strings.get('exclude')
        only_query_string = query_strings.get('only')

        only = only_query_string.split(',') if type(only_query_string) is str else []
        exclude = exclude_query_string.split(',') if type(exclude_query_string) is str else []

        return {
            'max_kcal': int(query_strings.get('maxkcal', default_filter.get('max_kcal'))),
            'max_price': float(query_strings.get('maxprice', default_filter.get('max_price'))),
            'as_json': str2bool(query_strings.get('json', 'true')),
            'only': only,
            'exclude': exclude
        }

    return default_filter


def filter_dishes_by_user_filters(all_dishes, filters):
    filtered_dishes = [
        dish
        for dish in all_dishes
        if
        dish.is_cheaper_than(filters.get('max_price'))
        and dish.has_less_kcal_than(filters.get('max_kcal'))
        and filter_dishes(filters.get('only'), dish, True)
        and not filter_dishes(filters.get('exclude'), dish, False)
    ]
    return filtered_dishes