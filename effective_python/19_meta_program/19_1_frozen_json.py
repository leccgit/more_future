import keyword
from collections import abc


class FrozenJSON:
    def __init__(self, mapping: abc.Mapping):
        self.__data = {}
        for key, val in mapping.items():
            if keyword.iskeyword(key):
                key = "__" + key
            self.__data[key] = val

    def __getattr__(self, name):
        if hasattr(self.__data, name):
            # 获取 __data的实例属性
            return getattr(self.__data, name)
        else:
            # 可能会抛出 KeyError
            return self.build(self.__data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)
        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj


if __name__ == '__main__':
    grad = FrozenJSON({'name': 'Jim Bo', 'class': 1982, "ages": [1, 2, 34]})
    print(grad.__class)
    print(grad.keys())
