from time import time
from functools import wraps
from asyncio import iscoroutinefunction


def time_costs(f):
    @wraps(f)
    def running_fun(*args, **kwargs):
        start_time = time()
        result = f(*args, **kwargs)
        end_time = time()
        try:
            print('function {} costs {}s'.format(f.__name__, end_time - start_time))
        except AttributeError:
            print('function {}  costs {}s'.format(f.__name__, end_time - start_time))
        return result

    @wraps(f)
    async def running_async_fun(*args, **kwargs):
        start_time = time()
        result = await f(*args, **kwargs)
        end_time = time()
        try:
            print('function {} costs {}s'.format(f.__name__, end_time - start_time))
        except AttributeError:
            print('function {}  costs {}s'.format(f.__name__, end_time - start_time))

        return result

    return running_async_fun if iscoroutinefunction(f) else running_fun
