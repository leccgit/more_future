from datetime import datetime
from redis_dict import redis_dict_create

REDIS_ENCODING_RAW = 0

# 对象的数据类型
REDIS_STRING = 0
REDIS_LIST = 1
REDIS_SET = 2
REDIS_ZSET = 3
REDIS_HASH = 4


def LRU_CLOCK():
    return datetime.now()


class RedisObject:
    __slots__ = ("type", "encoding", "lru", "refcount", "ptr",)

    def __init__(self):
        self.type = None  # 类型
        self.encoding = None  # 编码
        self.lru = None  # 最后一次访问时间 datetime(在py)
        self.refcount = 0  # 引用次数
        self.ptr = None  # 指向实际值的指针


def create_object(value_type, ptr):
    redis_object = RedisObject()
    redis_object.type = value_type
    redis_object.encoding = REDIS_ENCODING_RAW
    redis_object.ptr = ptr
    redis_object.refcount = 1
    redis_object.lru = LRU_CLOCK()
    return redis_object


def create_hash_object() -> RedisObject:
    r_dict = redis_dict_create(None, None)
    o = create_object(REDIS_HASH, r_dict)
    o.encoding = None  # 该处没有进行实现
    return o


if __name__ == '__main__':
    redis_dict = create_hash_object()
    print(redis_dict.lru)
