from inspect import getgeneratorstate
from collections import namedtuple

Result = namedtuple("Result", "count average")


# 子生成器
def average():
    total = 0.0
    count = 0
    avg = None
    while True:
        item = yield
        if item is None:
            break
        total += item
        count += 1
        avg = total / count
    # raise StopIteration(Result(count, avg)) yield from会catch StopIteration, 而其他的异常则会向上冒泡，传给委派生成器
    return Result(count, avg)


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from average()


# 输出报告
def report(results):
    for key, result in sorted(results.items()):
        group, unit = key.split(';')
        print('{:2} {:5} averaging {:.2f}{}'.format(
            result.count, group, result.average, unit))


# 客户端调用
def main(records: dict):
    result = {}
    for key, values in records.items():
        group = grouper(result, key)
        next(group)  # 预激协程
        for val in values:
            group.send(val)
        # print(getgeneratorstate(group))
        group.send(None)  # 协程的终止条件，避免yield from调用的协程生成器阻塞
    report(result)


data = {
    'girls;kg':
        [40.9, 38.5, 44.3, 42.2, 45.2, 41.7, 44.5, 38.0, 40.6, 44.5],
    'girls;m':
        [1.6, 1.51, 1.4, 1.3, 1.41, 1.39, 1.33, 1.46, 1.45, 1.43],
    'boys;kg':
        [39.0, 40.8, 43.2, 40.8, 43.1, 38.6, 41.4, 40.6, 36.3],
    'boys;m':
        [1.38, 1.5, 1.32, 1.25, 1.37, 1.48, 1.25, 1.49, 1.46],
}
if __name__ == '__main__':
    main(data)
