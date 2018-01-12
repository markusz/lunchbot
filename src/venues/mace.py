import re

from datetime import datetime
from src.models.dish import Dish

from src.utils.pdf_util import url_to_pypdf
from src.utils.text_util import extract_data_from_text

url = "http://mace-restaurant.de/wp-content/uploads/2015/08/MACE_Tageskarte.pdf"

def get_lunch_for_date(date=datetime.now(), show_only_current_day=True):
    reader = url_to_pypdf(url)
    text = reader.getPage(0).extractText()

    reduced_string = re.sub(r'Tagespizza|Tagesempfehlung|Tageskarte am [0-9]{2}.[0-9]{2}.[0-9]{4}', '', text)
    reduced_string = re.sub(r'\n', ' ', reduced_string)
    types = re.match(r".+?(MACE Restaurant+?)(.+?)(MACE Kitchen)+?(.+?)$", reduced_string)

    restaurant = re.findall(r'(.+?)([0-9]+,[0-9]{2})( Euro)',  types.group(2))
    kitchen = re.findall(r'(.+?)([0-9]+,[0-9]{2})( Euro)',  types.group(4))

    dishes = []

    rest_dishes = [
        Dish(
            'MACE (Restaurant)',
            extract_data_from_text(res[0].strip())[0],
            extract_data_from_text(res[0].strip())[1],
            price=float(res[1].replace(',','.')),
            src=url
        )
        for res
        in restaurant
        if extract_data_from_text(res[0].strip())[0][0].isupper()
    ]

    kit_dishes = [
        Dish(
            'MACE (Kitchen)',
            extract_data_from_text(res[0].strip())[0],
            extract_data_from_text(res[0].strip())[1],
            price=float(res[1].replace(',','.')),
            src=url
        )
        for res
        in kitchen
        if extract_data_from_text(res[0].strip())[0][0].isupper()
    ]

    dishes.extend(rest_dishes)
    dishes.extend(kit_dishes)

    return dishes
