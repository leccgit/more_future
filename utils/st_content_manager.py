from contextlib import contextmanager


class ContextManageTest:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        """

        :param exc_type: 异常类， 例如  ValueError
        :param exc_val: 异常实例。有时会有参数传给异常构造方法，
            例如错误消息，这些参数可以使用 exc_value.args 获取
        :param exc_tb: traceback 对象
        :return:
        """
        pass


@contextmanager
def looking_glass():
    """
    示例有一个严重的错误：如果在 with 块中抛出了异常，Python 解释器会将其捕获，
    然后在 looking_glass 函数的 yield 表达式里再次抛出。但是，那里没有处理错误的代码，
    因此 looking_glass 函数会中止，永远无法恢复成原来的 sys.stdout.write 方法，导致系统处于无效状态。
    :return:
    """
    import sys
    original_write = sys.stdout.write

    def reverse_write(text):
        original_write(text[::-1])

    sys.stdout.write = reverse_write
    yield "ABCDEFG"  # 该处没有处理错误的方法
    sys.stdout.write = original_write


try:
    with looking_glass() as what:
        print("lei, this is my name!")
        print(what)
        raise StopIteration
except Exception as e:
    print("123")  # -> 321, looking_glass()中没有对错误进行异常处理，
    print(str(e))
