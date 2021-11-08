import time
from functools import wraps
from random import randint
from asyncio import gather, get_event_loop, sleep, iscoroutinefunction


def time_cost(func):
    @wraps(func)
    async def await_time_cost(*args, **kwargs):
        start_time = time.time()
        _result = await func(*args, **kwargs)
        end_time = time.time()
        print("async func:{} cost time is {}".format(func.__name__, end_time - start_time))
        return _result

    @wraps(func)
    def wait_time_cost(*args, **kwargs):
        start_time = time.time()
        _result = func(*args, **kwargs)
        end_time = time.time()
        print("sync func:{} cost time is {}".format(func.__name__, end_time - start_time))
        return _result

    return await_time_cost if iscoroutinefunction(func) else wait_time_cost


@time_cost
async def find_all_records_with_gather():
    """
    使用gather
    :return:
    """

    async def task_func(res: list):
        a = await find_one_record()
        res.append(a)

    c_result = []
    all_tasks = []
    for _ in range(1000):
        all_tasks.append(task_func(c_result))
    await gather(*all_tasks)
    return c_result


@time_cost
async def find_all_records_not_gather():
    """
    不使用gather
    :return:
    """
    c_result = []
    for _ in range(20):
        c_result.append(await find_one_record())
    return c_result


async def find_one_record(_sleep_time=.1):
    """
    使用 asyncio.sleep 模拟异步的io操作,
    :param _sleep_time:
    :return:
    """
    await sleep(_sleep_time)
    return randint(0, 20)


if __name__ == '__main__':
    current_loop = get_event_loop()
    all_test_tasks = [find_all_records_with_gather(), find_all_records_not_gather()]
    current_loop.run_until_complete(gather(*all_test_tasks))
    current_loop.close()
