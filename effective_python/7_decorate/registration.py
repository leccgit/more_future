registry = []


def register(func):
    print('[1]running register(%s)' % func)
    registry.append(func)
    return func


@register
def f1():
    print('[4] running f1()')


@register
def f2():
    print('[5] running f2()')


def f3():
    print('[6] running f3()')


def main():
    print('[2] running main()')
    print('[3] registry ->', registry)
    f1()
    f2()
    f3()


if __name__ == '__main__':
    main()
