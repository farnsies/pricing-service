__author__ = 'mrf'

from typing import TypeVar, Type, List, Union
from abc import ABCMeta, abstractmethod
from common.database import Database

T = TypeVar('T', bound="Model")


class Model(metaclass=ABCMeta):
    collection: str
    _id: str

    def __init__(self, *args, **kwargs):
        pass

    def persist(self):
        Database.update(self.collection, {"_id": self._id}, self.json())

    def remove_from_db(self):
        Database.remove(self.collection, {"_id": self._id})

    @abstractmethod
    def json(self) -> dict:
        raise NotImplementedError

    @classmethod
    def get_by_id(cls: Type[T], _id: str) -> T:
        return cls.find_one_by("_id", _id)

    @classmethod
    def all(cls: Type[T]) -> List[T]:
        elements_from_db = Database.find(cls.collection, {})
        return [cls(**element) for element in elements_from_db]

    @classmethod
    def find_one_by(cls: Type[T], attr: str, value: Union[str, dict]) -> T:
        return cls(**Database.find_one(cls.collection, {attr: value}))

    @classmethod
    def find_many_by(cls: Type[T], attr: str, value: Union[str, dict]) -> List[T]:
        return [cls(**element) for element in
                Database.find(cls.collection, {attr: value})]
