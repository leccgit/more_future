#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from hashlib import sha1
from functools import wraps
from redis import Redis, ConnectionPool
from redis.exceptions import NoScriptError
from distutils.version import StrictVersion

# Adapted from http://redis.io/commands/incr#pattern-rate-limiter-2
INCREMENT_SCRIPT = b"""
    local current
    current = tonumber(redis.call("incrby", KEYS[1], ARGV[2]))
    if current == tonumber(ARGV[2]) then
        redis.call("expire", KEYS[1], ARGV[1])
    end
    return current
"""
INCREMENT_SCRIPT_HASH = sha1(INCREMENT_SCRIPT).hexdigest()


class TooManyRequests(Exception):
    """
    连接数过多
    """
    pass


def redis_version_check(redis_cnn) -> bool:
    """
    校验redis的版本, 低版本的redis无法使用EVALSHA和EVAL命令
    :return: bool
    """
    redis_version = redis_cnn.info()['redis_version']
    is_supported = StrictVersion(redis_version) >= StrictVersion('2.6.0')
    return bool(is_supported)


def redis_rate_limit(
        unique_key: str,
        source_name: str = '',
        once_incr: int = 1,
        max_requests: int = 60,
        expire: int = 60,
        redis_pool: ConnectionPool = None
):
    """
    针对redis版本高于2.6.0所做的函数限流器
    ps: 也可以修改为接口限流器, 需要修改实现
    客户端ip, 这种参数应该由request请求对象中进行获取, 或者是其他能标识用户唯一id的参数
    :param unique_key: 客户端ip
    :param source_name: 装饰的接口函数
    :param once_incr: 调用次数增加
    :param max_requests: 最大调用次数
    :param expire: 过期时间
    :param redis_pool: redis连接池
    :return:
    """
    if once_incr > max_requests:
        raise ValueError("once_incr:{once_incr} overflows max_requests of {max_requests}!"
                         .format(once_incr=once_incr, max_requests=max_requests))
    elif once_incr <= 0:
        raise ValueError("{once_incr} is not a valid increment, should be greater than or equal to zero!"
                         .format(once_incr=once_incr))
    redis_cnn = Redis(connection_pool=redis_pool)
    redis_version_check(redis_cnn)

    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            try:
                current_usage = wrapped.redis_cnn.evalsha(
                    INCREMENT_SCRIPT_HASH, 1, wrapped.rate_limit_key, wrapped.expire, wrapped.once_incr)
            except NoScriptError:
                current_usage = wrapped.redis_cnn.eval(
                    INCREMENT_SCRIPT, 1, wrapped.rate_limit_key, wrapped.expire, wrapped.once_incr)

            if int(current_usage) > wrapped.max_requests:
                raise TooManyRequests()
            return fn(*args, **kwargs)

        wrapped.unique_key = unique_key
        wrapped.source_name = source_name
        if not wrapped.source_name:
            wrapped.source_name = fn.__name__
        if not wrapped.source_name:
            raise ValueError("source_name:{source_name} is not valid, should not be empty!"
                             .format(source_name=source_name))
        wrapped.max_requests = max_requests
        wrapped.expire = expire
        wrapped.redis_cnn = redis_cnn
        wrapped.once_incr = once_incr
        wrapped.rate_limit_key = "rate_limit:{0}_{1}".format(wrapped.source_name, wrapped.unique_key)

        return wrapped

    return wrapper


if __name__ == '__main__':
    REDIS_POOL = ConnectionPool(host='127.0.0.1', port=6379, db=0)


    @redis_rate_limit(unique_key='127.0.0.1', redis_pool=REDIS_POOL)
    def api_call_back():
        pass


    for i in range(1):
        api_call_back()
