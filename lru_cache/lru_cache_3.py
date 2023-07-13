from collections import OrderedDict


class CacheDeduplication:
    def __init__(self, max_size: int = 2000):
        self.cache = OrderedDict()
        self.max_size = max_size

    def add(self, item) -> bool:
        if item in self.cache:
            return False

        self.del_redundant()
        self.cache[item] = None
        return True

    def del_redundant(self):
        if len(self.cache) <= self.max_size * 2:
            return
        while len(self.cache) >= self.max_size:
            if self.cache:
                self.cache.popitem(last=False)


if __name__ == '__main__':
    from random import randint
    from time import sleep

    t_cache = CacheDeduplication(max_size=2000)
    while True:
        point = (randint(0, 1000), randint(0, 9))
        add_suc = t_cache.add(point)
        if add_suc:
            print(f"数据推送成功, 长度: {len(t_cache.cache)} 数据:{point}")
        else:
            print(f"数据重复, 数据:{point}")
