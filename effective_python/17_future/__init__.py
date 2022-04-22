def run(func):
    try:
        result = func()
        if result is not None:
            from tornado.gen import convert_yielded
            result = convert_yielded(result)
    except Exception:
        import sys
        print('Exception,{}'.format(sys.exc_info()))
    else:
        print("else")


async def demo():
    print("112")


if __name__ == '__main__':
    run(demo())
