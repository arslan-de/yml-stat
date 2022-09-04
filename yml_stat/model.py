"""
YML model
---------
Root
- Catalog
 - Shop
   - Categories
     - List[Category]
        id: str
        parentId: str
        value: str
   - Offers
     - List[Offer]
        name: str
        categoryId: str
------------------
Raw data
---------
<yml_catalog>
    <shop>
        <categories>
            <category id="1">Обувь</category>
            <category id="2">Одежда</category>
            <category id="11" parentId="1">Кроссовки</category>
        </categories>
        <offers>
            <offer id="123456">
                <categoryId>11</categoryId>
            </offer>
        </offers>
    </shop>
</yml_catalog>
"""

from pydantic import BaseModel
from typing import List


class Category(BaseModel):
    id: str
    parentId: str = ""
    value: str


class Offer(BaseModel):
    name: str
    categoryId: str


class Categories(BaseModel):
    category: List[Category]


class Offers(BaseModel):
    offer: List[Offer]


class Shop(BaseModel):
    categories: Categories
    offers: Offers


class Catalog(BaseModel):
    shop: Shop


class Root(BaseModel):
    yml_catalog: Catalog
