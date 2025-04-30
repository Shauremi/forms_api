import abc

from src.users.schemas import User


class Repository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def add(self, user: User):
        pass

    @abc.abstractmethod
    def delete(self, _id: int):
        pass

    @abc.abstractmethod
    def update(self, _id: int, user: User):
        pass

    @abc.abstractmethod
    def read(self, _id: int):
        pass

    @abc.abstractmethod
    def list_users(self):
        pass
