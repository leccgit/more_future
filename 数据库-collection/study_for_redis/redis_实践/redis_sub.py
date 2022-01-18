#!/usr/bin/env python
#  -*- coding: utf-8 -*-

from redis import Redis, ConnectionPool

if __name__ == '__main__':
    REDIS_POOL = ConnectionPool(host='127.0.0.1', port=6379, db=1)

    redis_cnn = Redis(connection_pool=REDIS_POOL)
    sub = redis_cnn.pubsub()
    sub.psubscribe("test_notify", "test*")
    for item in sub.listen():
        print(item['channel'])
        print(item['data'])
        sub.unsubscribe()
    print("sub suc....")
