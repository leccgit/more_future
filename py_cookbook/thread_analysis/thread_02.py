import threading
import time


class InitThread(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, *, daemon=None):
        super(InitThread, self).__init__(group, target, name)

    def run(self) -> None:
        """线程的入口, 继承的线程提供覆盖, 来实现自己的逻辑"""
        print('this thread is {}!'.format(threading.currentThread().getName()))
        super(InitThread, self).run()


def print_func():
    time.sleep(1)
    print('exist: {}, is ending!'.format(threading.currentThread().getName()))


for i in range(3):
    # 针对创建的线程, 默认会生成一个线程名称, 也能指定创建的线程名称
    cur_thread = InitThread(target=print_func, name='is_{}_thread'.format(i))
    cur_thread.start()
    # cur_thread.join(timeout=0.5)  # 堵塞当前线程, 直到调用join的线程停止
print('end!')
