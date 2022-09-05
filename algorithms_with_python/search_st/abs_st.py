from abc import ABCMeta, abstractmethod


class AbsST(metaclass=ABCMeta):
    @abstractmethod
    def put(self, key, val):
        pass

    @abstractmethod
    def get(self, key):
        pass

    @abstractmethod
    def delete(self, key):
        pass

    @abstractmethod
    def keys(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def is_empty(self) -> bool:
        pass

    def contains(self, item) -> bool:
        pass
