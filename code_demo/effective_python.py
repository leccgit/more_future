import json


# Str: bytes和str的转换辅助函数
def to_str(bytes_or_str) -> str:
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode("utf-8")
    else:
        value = bytes_or_str
    return value


def to_bytes(bytes_or_str) -> bytes:
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode("utf-8")
    else:
        value = bytes_or_str
    return value


# Dict
def dict_paths(paths: list, c_obj: dict):
    """
    根据paths获取字典中的指定值
    assert dict_paths(['a', 'b'], {"a": {"b": 2}}) == 2
    assert dict_paths(['a', 'b'], {"c": {"b": 2}}) is None
    :param paths:
    :param c_obj:
    :return:
    """
    assert isinstance(paths, list), "paths type must list!"
    if not paths:
        return None
    return _paths(paths, c_obj)


def _paths(paths: list, c_obj: dict):
    for path in paths:
        if c_obj and isinstance(c_obj, dict) and path in c_obj:
            c_obj = c_obj[path]
        else:
            return None
    return c_obj


def load_json_key(data, key):
    try:
        result_dict = json.loads(data)  # may raise ValueError
    except ValueError as e:
        raise KeyError from e
    return result_dict[key]  # may raise KeyError


if __name__ == '__main__':
    # a = {"1": "a", "2": "b", "3": "c"}
    # print({
    #     v: k
    #     for k, v in a.items()
    # })
    # print({
    #     v: k
    #     for k, v in sorted(a.items(), key=lambda o: o[0], reverse=True)
    # })
    # def current_func_result(num):
    #     return "123"

    # def print_current_num(num):
    #     a = yield num
    #     print("current is num:{}".format(a))
    #
    #
    # b = print_current_num(12)
    # print(b.__next__())
    # next(b)
    # print(next(b))
    # next(b)
    # print(b.send(12))
    # def yield_test(num):
    #     yield num


    def gen_test():
        for i in range(3):
            c = yield i
            print("idx:{}, current is one test".format(c))


    g = gen_test()
    print(g.send(None))
    print(g.send("a"))
    print(g.send("b"))
    print(g.send("c"))

    # print(next(g))
    # print(next(g))
    # print(next(g))
