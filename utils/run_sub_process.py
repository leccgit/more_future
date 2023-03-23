import asyncio
import time
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from typing import Callable, List, Tuple


class SubProcessPoolExecutor(ProcessPoolExecutor):
    pass


def demo_01():
    st_time = time.time()
    i = 1
    while i < 200000000:
        i += 1
    # for _ in range(5):
    #     time.sleep(1)
    print("this is demo_01 cost time:{}".format(time.time() - st_time))


def demo_02():
    st_time = time.time()
    for _ in range(5):
        time.sleep(1)
    print("this is demo_02 cost time:{}".format(time.time() - st_time))


async def asyncio_with_sub_process(loop, blocking_tasks: List[Tuple[Callable, ...]]):
    do_tasks = []
    with ProcessPoolExecutor(len(blocking_tasks)) as executor:

        for block_task in blocking_tasks:
            do_tasks.append(
                loop.run_in_executor(executor, *block_task)
            )
        # for p in executor._processes.values():
        #     p.Process.name = "this_is_one_test_{}".format(time.time())
        print(executor._processes)
        for p in executor._processes.values():
            p.name = "this_is_test_{}".format(time.time())
        print(executor._processes)

    await asyncio.gather(*do_tasks)


async def asyncio_with_sub_thread(loop, blocking_tasks: List[Tuple[Callable, ...]]):
    do_tasks = []
    with ThreadPoolExecutor(len(blocking_tasks)) as executor:
        for block_task in blocking_tasks:
            do_tasks.append(
                loop.run_in_executor(executor, *block_task)
            )
    await asyncio.gather(*do_tasks)


if __name__ == '__main__':
    t = time.time()
    current_loop = asyncio.get_event_loop()
    # 进程执行器
    current_loop.run_until_complete(asyncio_with_sub_process(current_loop, [(demo_01,), (demo_01,), (demo_02,)]))
    # 线程执行器
    # current_loop.run_until_complete(asyncio_with_sub_thread(current_loop, [(demo_01,),(demo_01,), (demo_02,)]))

    current_loop.close()
    print("test cost time:{}".format(time.time() - t))
