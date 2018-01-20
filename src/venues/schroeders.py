import re
from datetime import datetime

from src.models.dish import Dish
from src.utils.pdf_util import url_to_pypdf
from src.utils.text_util import extract_data_from_text

url = "http://schroeders-restaurant.com/wp-content/uploads/2017/06/Schroeders-Wochenkarte.pdf"


def process_single_day_from_pdf(day_string):
    stripped = day_string.strip()
    splitted = re.split(r'Gericht [0-9]', stripped)

    # Removes double spaces and empty/short strings
    filtered_content = [
        re.sub(r' {2,}', ' ', x).strip()
        for x
        in splitted
        if len(x.strip()) > 3
    ]

    # Removes Drink der Woche / Dessert
    filtered_content = [
        re.sub('(Unser Drink der Woche|Dessert)(.+?)$', '', x).strip()
        for x
        in filtered_content
    ]

    # Prices can not be extracted properly from PDF -> omit them
    filtered_content = [
        re.sub(' [0-9]+$', '', x)
        for x
        in filtered_content
    ]

    return filtered_content


def get_lunch_for_date(date=datetime.now(), show_only_current_day=True):
    reader = url_to_pypdf(url)
    text = reader.getPage(0).extractText()
    dishes = []

    reduced_string = re.sub(r'Tagespizza|Tagesempfehlung|Tageskarte am [0-9]{2}.[0-9]{2}.[0-9]{4}', '', text)
    reduced_string = re.sub(r'\n', ' ', reduced_string)

    m = re.match(r"(.+?)Montag+?(.+?)Dienstag+?(.+?)Mittwoch+?(.+?)Donnerstag+?(.+?)Freitag+?(.+)", reduced_string)

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
                dishes.append(Dish('Schroeders', splitted[0], splitted[1], src=url))

    return dishes
