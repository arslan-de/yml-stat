import pandas as pd
import requests
import xmltodict
import xml
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


def prepare_category_data(categories: list) -> list:
    """
    Prepare category name fields
    :param categories:
    :return: List
        [(Id_1, Name_1), .. , (Id_N, Name_N)]
    """
    categories_dict = {category.id: (category.parentId, category.value) for category in categories}

    category_data = []
    for id_, value in categories_dict.items():
        parent, name = value
        new_name = get_full_name(categories_dict, parent, name) if parent else name
        category_data.append((id_, new_name))

    return category_data


def get_categories_summary(yml: dict) -> pd.DataFrame:
    """
    Prepare summarise table from raw-dict-data
    :param yml:
    :return: pd.DataFrame
        category    object
        offers      float64
        dtype: object
    """
    try:
        root: Root = Root.parse_obj(yml)
    except ValidationError as error:
        print(f"Incorrect YML data - {yml}")
        raise ValidationError(error)

    categories: list = root.yml_catalog.shop.categories.category
    category_df = pd.DataFrame(data=prepare_category_data(categories),
                               columns=["Id", "Name"]).set_index("Id")

    offers_list: list = root.yml_catalog.shop.offers.offer
    offer_df = pd.DataFrame(data=[(offer.categoryId, offer.name) for offer in offers_list],
                            columns=["categoryId", "Name"]).set_index("categoryId")
    offer_df = offer_df.groupby(["categoryId"]).count()

    result = category_df.merge(offer_df, how="left", left_on="Id", right_on="categoryId")\
        .rename(columns={"Name_x": "category", "Name_y": "offers"})\
        .fillna(value={"offers": 0})\
        .sort_values(by=["category"])

    return result


def get_yml_statistics(url: str) -> pd.DataFrame:
    """
    Create yml-file summary table
    :param url: path to yml-file with data
    :return: pd.DataFrame
        category    object
        offers      float64
        dtype: object
    """
    try:
        request: str = requests.get(url).text
    except requests.exceptions.ConnectionError as error:
        print(f"Incorrect url: {url}")
        raise requests.exceptions.ConnectionError(error)

    try:
        yml_string: dict = xmltodict.parse(request, attr_prefix="", cdata_key="value")
    except xml.parsers.expat.ExpatError as error:
        print(f"Parsing error {request}")
        raise xml.parsers.expat.ExpatError(error)

    categories_summary = get_categories_summary(yml_string)

    return categories_summary
