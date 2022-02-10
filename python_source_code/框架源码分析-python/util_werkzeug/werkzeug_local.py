from werkzeug.local import LocalStack, LocalProxy
import logging, random, threading, time

# 定义logging配置
logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-10s) %(message)s', )
# 生成一个LocalStack实例_stack
_stack = LocalStack()


class RequestContext(object):
    """
    定义一个requestContext类, 类包含一个上下文环境
    调用该类的实例, 会将上下文对象放入到_stack栈中去, 推出该上下文环境时, 栈将pop其中的上下文对象
    """

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __enter__(self):
        _stack.push(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is None:
            _stack.pop()

    def __repr__(self):
        return '%s, %s, %s' % (self.a, self.b, self.c)


# 定义一个可供不同线程调用的方法。当不同线程调用该
# 方法时，首先会生成一个RequestContext实例，并在这
# 个上下文环境中先将该线程休眠一定时间，之后打印出
# 目前_stack中的信息，以及当前线程中的变量信息。
# 以上过程会循环两次。
def worker(i):
    with request_context(i):
        for j in range(2):
            pause = random.random()
            logging.debug('Sleeping %0.02f', pause)
            time.sleep(pause)
            logging.debug('stack: %s' % _stack._local.__storage__.items())
            logging.debug('ident_func(): %d' % _stack.__ident_func__())
            logging.debug('a=%s; b=%s; c=%s' %
                          (LocalProxy(lambda: _stack.top.a),
                           LocalProxy(lambda: _stack.top.b),
                           LocalProxy(lambda: _stack.top.c)))
    logging.debug('Done')


# 调用该函数生成一个RequestContext对象
def request_context(i):
    i = str(i + 1)
    return RequestContext('a' + i, 'b' + i, 'c' + i)


# 在程序最开始显示_stack的最初状态
logging.debug('Stack Initial State: %s' % _stack._local.__storage__.items())
# 产生两个线程，分别调用worker函数
for i in range(2):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
main_thread = threading.currentThread()
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
# 在程序最后显示_stack的最终状态
logging.debug('Stack Finally State: %s' % _stack._local.__storage__.items())
