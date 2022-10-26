import asyncio
from asyncio import Lock as ALock
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


async def un_block_thread_with_ALock():
    """
    不同于Lock, RLock只会在首次请求的时候获取一把锁, 重复的加锁操作不会重复请求获取锁
    """
    main_thread = ALock()

    async with main_thread:
        for i in range(10):
            print('[{}]: now is {}......'.format(i, datetime.now()))
    print('thread end!')


if __name__ == '__main__':
    # un_block_thread_with_RLock()
    current_loop = asyncio.get_event_loop()
    current_loop.run_until_complete(un_block_thread_with_ALock())
    current_loop.close()
