import keyword
from collections import abc, deque
from typing import List
from copy import deepcopy


class FrozenJSON:
    def __init__(self, mapping: abc.Mapping):
        self.__data = {}
        for key, val in mapping.items():
            if keyword.iskeyword(key):
                # 针对python的关键字，进行替换别名
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


def dict_path(mapping: abc.Mapping, paths: List):
    if not mapping:
        return
    if not paths:
        return mapping

    path_deque = deque(paths)
    travel_mapping = deepcopy(mapping)
    while path_deque:
        path_name = path_deque.popleft()
        travel_mapping = travel_mapping[path_name]

    return travel_mapping


if __name__ == '__main__':
    front_dict = {'name': 'Jim Bo', 'class': 1982, "ages": [1, 2, 34], "like": {"food": "apple", "age": [1, 2, 3]}}

    grad = FrozenJSON(front_dict)
    print(grad.__class)
    print(grad.keys())
    print(grad.like.food)
    print(grad.ages[0])
    print("demo", grad.ages)
    print("demo", grad.like)

    print(dict_path(front_dict, ["like", "food"]))
    print(dict_path(front_dict, ["ages", 0]))
    print(dict_path(front_dict, ["class"]))
