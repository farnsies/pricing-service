__author__ = "mrf"

import re
import uuid
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup
from common.database import Database
from models.model import Model

CURRENCY_REGEX = r"((\d+,)*\d+\.\d{2})"
CURRENCY = re.compile(CURRENCY_REGEX)


@dataclass(eq=False)
class Item(Model):
    collection: str = field(init=False, default="items")
    url: str
    tag_name: str
    query: dict
    price: float = field(default=None)
    _id: str = field(default_factory=lambda: uuid.uuid4().hex)

    def load_price(self) -> float:
        response = requests.get(self.url)
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        element = soup.find(self.tag_name, self.query)

        string_price = element.text.strip()
        match = CURRENCY.search(string_price)
        price = match.group(1)
        self.price = float(price.replace(",", ""))
        return self.price

    def json(self) -> dict:
        return {
            "_id": self._id,
            "url": self.url,
            "tag_name": self.tag_name,
            "price": self.price,
            "query": self.query
        }

    def persist(self):
        Database.insert(self.collection, self.json())

    @classmethod
    def get_by_id(cls, _id):
        item_json = Database.find_one("items", {"_id": _id})
        return cls(**item_json)
