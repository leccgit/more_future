from time import time, sleep, strftime
from concurrent import futures


def display(*args):
    print(strftime('[%H:%M:%S]'), end=' ')
    print(*args)


def loiter(n):
    msg = '{}loiter({}): doing nothing for {}s...'
    display(msg.format('\t' * n, n, n))
    sleep(n)
    msg = '{}loiter({}): done.'
    display(msg.format('\t' * n, n))
    return n * 10


def main():
    display("*" * 10 + 'Script starting.' + "*" * 10)
    st = time()
    with futures.ThreadPoolExecutor(max_workers=3) as executor:
        res = executor.map(loiter, range(5))
        display('results:', res)
        display('Waiting for individual results:')
        for i, result in enumerate(res):
            display('result {}: {}'.format(i, result))
    display("cost_time:{}".format(time() - st))


if __name__ == '__main__':
    main()
