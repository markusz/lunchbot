import re

from datetime import datetime
from src.models.dish import Dish

from src.utils.pdf_util import url_to_pypdf
from src.utils.text_util import extract_data_from_text

url = "http://www.comfort-hotel-am-medienpark.de/images/pdf/Wochenkarte.pdf"


def process_single_day_from_pdf(day_string):
    stripped = day_string.strip()
    extracted = re.sub(r"Jeden (.+) von 12-14 Uhr", '', stripped)

    # Splits around nutrition information of the form A1,C,D,E,1,2,3
    splitted = re.split(r'[A-Z]([0-9]|[A-Z]+|,|-)+', extracted)
    filtered_content = [x.strip().replace('  ', ' ') for x in splitted if 150 > len(x.strip()) > 3]

    return filtered_content


def idx_to_name_of_day(idx):
    if idx == 0:
        return 'Montag'
    if idx == 1:
        return 'Dienstag'
    if idx == 2:
        return 'Mittwoch'
    if idx == 3:
        return 'Donnerstag'
    if idx == 4:
        return 'Freitag'


def extracted_text_to_items(text, date=None):
    dishes = []
    joined = ''.join(text)

    m = re.match(r"(.+?)Montag+?(.+?)Dienstag+?(.+?)Mittwoch+?(.+?)Donnerstag+?(.+?)Freitag+?(.+)Alle Preise verstehen+?(.+)", joined)

    monday = process_single_day_from_pdf(m.group(2))
    tuesday = process_single_day_from_pdf(m.group(3))
    wednesday = process_single_day_from_pdf(m.group(4))
    thursday = process_single_day_from_pdf(m.group(5))
    friday = process_single_day_from_pdf(m.group(6))

    items_per_day = [monday, tuesday, wednesday, thursday, friday]

    for idx, day in enumerate(items_per_day):
        if date is None or idx == date.weekday():
            for item in day:
                splitted = extract_data_from_text(item)
                if splitted[0][0].isupper():
                    dishes.append(Dish('Hacker', splitted[0], splitted[1] if len(splitted) > 1 else None,src=url))

    return dishes


def get_lunch_for_date(date=datetime.now(), show_only_current_day=True):
    reader = url_to_pypdf(url)
    contents = reader.getPage(0).extractText().split('\n')
    return extracted_text_to_items(contents, date if show_only_current_day else None)
