from datetime import datetime
from threading import Lock, RLock


def block_thread_with_lock():
    main_thread = Lock()

    main_thread.acquire()
    for i in range(10):
        main_thread.acquire()
        print('[{}]: now is {}......'.format(i, datetime.now()))
        main_thread.release()
    main_thread.release()
    print('thread end!')


def un_block_thread_with_RLock():
    """
    不同于Lock, RLock只会在首次请求的时候获取一把锁, 重复的加锁操作不会重复请求获取锁
    """
    main_thread = RLock()

    main_thread.acquire()
    for i in range(10):
        main_thread.acquire()
        print('[{}]: now is {}......'.format(i, datetime.now()))
        main_thread.release()
    main_thread.release()
    print('thread end!')
    main_thread.release()  # raise RuntimeError


if __name__ == '__main__':
    un_block_thread_with_RLock()
