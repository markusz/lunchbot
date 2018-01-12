import re


def extract_data_from_text(text):
    text = re.sub(r' {2,}', ' ', text)
    m = re.match(r'((.+?) (mit|-|auf) ?(.+)?|(.+))', text)

    if m.group(2) is not None:
        result = (m.group(2), m.group(4))
    else:
        result = (m.group(1), None)

    return result
