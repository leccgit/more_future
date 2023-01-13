import time
from asyncio import iscoroutinefunction
from functools import wraps


def time_costs(f):
    @wraps(f)
    def running_fun(*args, **kwargs):
        s = time.perf_counter()
        try:
            result = f(*args, **kwargs)
            return result
        except Exception as e:
            print(f'function {f.__name__} operate error:{str(e)}')
        finally:
            elapsed = time.perf_counter() - s
            print(f'function {f.__name__} costs {elapsed:0.5f} seconds.')

    @wraps(f)
    async def running_async_fun(*args, **kwargs):
        s = time.perf_counter()
        try:
            result = await f(*args, **kwargs)
            return result
        except Exception as e:
            print(f'function {f.__name__} operate error:{str(e)}')
        finally:
            elapsed = time.perf_counter() - s
            print(f'function {f.__name__} costs {elapsed:0.5f} seconds.')

    return running_async_fun if iscoroutinefunction(f) else running_fun
