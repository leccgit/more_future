def func_a():
    pass


if __name__ == '__main__':
    func_a.name = 'leichao'
    func_a._cache = {}
    func_a._cache["age"] = 25
    print(func_a.name)
    print(func_a._cache)
