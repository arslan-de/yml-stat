import pandas as pd

from yml_stat.model import Root
from yml_stat.utils import get_full_name, parse_yml, get_file, get_model


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


def prepare_offers_data(offers: list) -> list:
    """
    Prepare offers Name and categoryId
    :param offers:
    :return:
    """
    return [(offer.categoryId, offer.name) for offer in offers]


def get_categories_summary(yml: dict) -> pd.DataFrame:
    """
    Prepare summarise table from raw-dict-data
    :param yml:
    :return: pd.DataFrame
        category    object
        offers      float64
        dtype: object
    """
    root: Root = get_model(yml)

    categories: list = root.yml_catalog.shop.categories.category
    category_df = pd.DataFrame(data=prepare_category_data(categories),
                               columns=["Id", "Name"]).set_index("Id")

    offers: list = root.yml_catalog.shop.offers.offer
    offer_df = pd.DataFrame(data=prepare_offers_data(offers),
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
    yml: dict = parse_yml(get_file(url))
    categories_summary = get_categories_summary(yml)

    return categories_summary
