import pytest
import pandas as pd

from yml_stat.main import prepare_category_data, get_categories_summary
from yml_stat.model import Category


class TestClassUtils:
    @pytest.mark.parametrize(
        "categories, expected_result",
        [(
            [Category(id='1', parentId='', value='Category'),
             Category(id='2', parentId='1', value='SubCategory'),
             Category(id='3', parentId='2', value='Leaf')],
            [('1', 'Category'), ('2', 'Category / SubCategory'), ('3', 'Category / SubCategory / Leaf')]
        )],
    )
    def test_prepare_category_data(self, categories, expected_result):
        assert prepare_category_data(categories) == expected_result

    @pytest.mark.parametrize(
        "yml, expected_result",
        [(
            {'yml_catalog':
                {'shop':
                    {'categories':
                        {'category': [
                            {'id': '1', 'parentId': '', 'value': 'Category'},
                            {'id': '2', 'parentId': '1', 'value': 'SubCategory'},
                            {'id': '3', 'parentId': '2', 'value': 'Leaf'}
                        ]
                        },
                        'offers':
                            {'offer': [
                                {'id': '174', 'name': 'Cisco 1A', 'categoryId': '3'},
                                {'id': '174', 'name': 'Cisco 2A', 'categoryId': '2'},
                                {'id': '174', 'name': 'Cisco 3A', 'categoryId': '3'}
                            ]
                            }}}},
            pd.DataFrame(data=[("Category", 0.0),
                               ("Category / SubCategory", 1.0),
                               ("Category / SubCategory / Leaf", 2.0)],
                         columns=["category", "offers"])
        )],
    )
    def test_get_categories_summary(self, yml, expected_result):
        summary_table = get_categories_summary(yml)
        assert list(summary_table["category"]) == list(expected_result["category"])
        assert list(summary_table["offers"]) == list(expected_result["offers"])
