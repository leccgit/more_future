from asyncio import Lock, gather, get_event_loop, iscoroutinefunction, sleep
from functools import wraps
from random import randint


class Context:
    data = {}
    do_list = []


def get_context(key: str):
    if key not in Context.data:
        return None
    return Context.data[key]


def update_context(key: str, val):
    Context.data[key] = val


def add_lock(process_func):
    @wraps(process_func)
    async def run(*args, **kwargs):
        lock_name = process_func.__name__
        if 'lock_id' in kwargs and kwargs.get('lock_id'):
            if kwargs.get('lock_id'):
                lock_name = kwargs.get('lock_id')
        mutex_context = get_context(lock_name)
        if mutex_context is None:
            mutex_context = Lock()
            update_context(lock_name, mutex_context)
        async with mutex_context:
            return await process_func(*args, **kwargs)

    return run


def raise_exception(f):
    @wraps(f)
    def running_fun(*args, **kwargs):
        try:
            result = f(*args, **kwargs)
        except Exception as e:
            print('Error occured in {} cause {}'.format(f.__name__, str(e)))
        else:
            return result

    @wraps(f)
    async def running_async_fun(*args, **kwargs):
        try:
            result = await f(*args, **kwargs)
        except Exception as e:
            print('Error occured in {} cause {}'.format(f.__name__, str(e)))
        else:
            return result

    return running_async_fun if iscoroutinefunction(f) else running_fun


@add_lock
async def compute_kpi(device_code: str, lock_id: str = None):
    await sleep(.2)
    return device_code


@raise_exception
async def process_point_pushing(msg):
    print(msg)
    if isinstance(msg, list):
        data_list = []
        cl_point = []
        gzm_point = []
        sxb_point = []
        trace_info = []
        for i in msg:
            i_code = i.get('code')
            if '~' in i_code:
                device, code_type = i_code.split('~')
                if code_type in ['g_sbzt', 'p_kgj_plc', 'p_kgj_wg']:
                    data_list.append({"code": i["code"], "value": i["value"], "timestamp": i["time_stamp"]})
                elif code_type in ['p_cl']:
                    cl_point.append({"code": i["code"], "value": i["value"], "timestamp": i["time_stamp"]})
                elif code_type in ['p_gzm']:
                    gzm_point.append({"code": i["code"], "value": i["value"], "timestamp": i["time_stamp"]})
                elif code_type in ['p_sxb_plc']:
                    sxb_point.append({"code": i["code"], "value": i["value"], "timestamp": i["time_stamp"]})
                elif code_type in ['p_product_info']:
                    trace_info.append({"code": i["code"], "value": i["value"], "timestamp": i["time_stamp"]})
        if not data_list and not cl_point and not gzm_point and not sxb_point and not trace_info:
            return
        await sleep(.2)


async def make_faker_data():
    while True:
        Context.do_list.append(
            [{"code": "device_1_1~p_kgj_wg", "value": 1, "time_stamp": "22020"},
             {"code": "device_1_1~g_sbzt", "value": "0,1,1,1,1,1,1,1", "time_stamp": "22020"}]
        )
        await sleep(0.01)


async def do_main():
    async for faker_data in make_faker_data():
        await process_point_pushing(faker_data)


if __name__ == '__main__':
    current_loop = get_event_loop()
    current_loop.run_until_complete(do_main())
    current_loop.close()
