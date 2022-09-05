import xml

import requests
import xmltodict
from pydantic import ValidationError

from yml_stat.model import Root


def get_full_name(categories_dict: dict, parent_id: str, prev_name: str) -> str:
    """
    Recursively get full category name from netted structure
    :param categories_dict:
    :param parent_id:
    :param prev_name:
    :return: str
        Category1 / .. / CategoryN
    """
    new_parent, new_name = categories_dict.get(parent_id, ("", ""))
    new_name = get_full_name(categories_dict, new_parent, f"{new_name} / {prev_name}") if new_name else prev_name

    return new_name


def parse_yml(yml: str) -> dict:
    """
    Get parsed from string to dict YML file
    :param yml:
    :return:
    """
    try:
        parsed_yml: dict = xmltodict.parse(yml, attr_prefix="", cdata_key="value")
    except xml.parsers.expat.ExpatError as error:
        print(f"Parsing error {yml}")
        raise xml.parsers.expat.ExpatError(error)

    return parsed_yml


def get_file(url: str) -> str:
    """
    Get file by URL
    :param url:
    :return:
    """
    try:
        file: str = requests.get(url).text
    except requests.exceptions.ConnectionError as error:
        print(f"Incorrect url: {url}")
        raise requests.exceptions.ConnectionError(error)

    return file


def get_model(yml: dict) -> Root:
    """
    Get parsed and fulfilled Root model
    :param yml:
    :return:
    """
    try:
        root: Root = Root.parse_obj(yml)
    except ValidationError as error:
        print(f"Incorrect YML data - {yml}")
        raise ValidationError(error)

    return root
