DICT_OK = 0  # hash表执行操作成功
DICT_ERR = 1  # hash表执行操作失败
dict_can_resize = 1  # hash表能执行扩容操作
LONG_MAX = 1024 * 1024  # 定义hash表的最大值
DICT_HT_INITIAL_SIZE = 4  # 初始化哈希表的大小
dict_force_resize_ratio = 5  # 强制 rehash 的比率


class RedisDictEntry:
    """ hash表中table保存的节点"""
    __slots__ = ('key', 'value', 'next')

    def __init__(self):
        self.key = None
        self.value = None
        self.next = None

    def __repr__(self):
        return "{%s:%s}" % (self.key, self.value)


class DictIterator:
    """
     如果 safe 属性的值为 1 ，那么在迭代进行的过程中，
     程序仍然可以执行 dictAdd 、 dictFind 和其他函数，对字典进行修改。
     如果 safe 不为 1 ，那么程序只会调用 dictNext 对字典进行迭代，
     而不对字典进行修改。
    """
    __slots__ = ('d', 'table', 'index', 'safe', 'entry', 'nextEntry')

    def __init__(self):
        self.d = None  # 被迭代的字典
        self.table = None  # 正在被迭代的哈希表号码，值可以是 0 或 1 。
        self.index = None  # 迭代器当前所指向的哈希表索引位置
        self.safe = None  # 标识这个迭代器是否安全
        self.entry = None  # 当前迭代到的节点的指针
        # 当前迭代节点的下一个节点
        # 因为在安全迭代器运作时， entry 所指向的节点可能会被修改，
        # 所以需要一个额外的指针来保存下一节点的位置，
        # 从而防止指针丢失
        self.nextEntry = None


class DictHt:
    """ hash表中的hash table """
    __slots__ = ('table', 'size', 'sizemask', 'used')

    def __init__(self):
        self.table = None  # 哈希表数组 内部保存的是 RedisDictEntry节点
        self.size = 0  # 哈希表大小
        self.sizemask = 0  # 哈希表大小掩码，用于计算索引值, 总是等于 size - 1
        self.used = 0  # 该哈希表已有节点的数量


class RedisDict:
    __slots__ = ('ht', 'type', 'privdata', 'rehashidx', 'iterators')

    def __init__(self):
        self.ht = [DictHt(), DictHt()]  # 哈希表
        self.type = None  # 设置类型特定函数
        self.privdata = None  # 私有数据
        self.rehashidx = -1  # rehash索引, 当rehash不在进行时，值为 -1
        self.iterators = 0  # 目前正在运行的安全迭代器的数量


def dict_hash_key(key):
    """
    针对Key的散列函数
    :param key:
    :return:
    """
    return abs(hash(key))


def redis_dict_create(type, privDataPtr) -> RedisDict:
    """
    创建一个redis结构的字典
    :return:
    """
    redis_dict = RedisDict()
    redis_dict_init(redis_dict, type, privDataPtr)
    return redis_dict


def redis_dict_init(redis_dict: RedisDict, type, privDataPtr):
    """
    初始化redis的字典
    :param redis_dict:
    :param type: 类型
    :param privDataPtr: 私有数据
    :return:
    """
    redis_dict_reset(redis_dict.ht[0])
    redis_dict_reset(redis_dict.ht[1])
    redis_dict.type = type
    redis_dict.privdata = privDataPtr
    redis_dict.rehashidx = -1
    redis_dict.iterators = 0
    return DICT_OK


def redis_dict_reset(hash_table: DictHt):
    """
    初始化hash table
    :param hash_table:
    :return:
    """
    hash_table.table = None
    hash_table.size = 0
    hash_table.sizemask = 0
    hash_table.used = 0


def redis_dict_add(redis_dict: RedisDict, key, value):
    """

    :param redis_dict:
    :param key:
    :param value:
    :return:
    """
    if redis_dict_is_rehashing(redis_dict):
        redis_dict_rehash_step(redis_dict)


def redis_dict_rehash_step(redis_dict: RedisDict):
    """
    同时跌的的数量为0的时候, 进行单步的rehash操作
    :param redis_dict:
    :return:
    """
    if redis_dict.iterators == 0:
        redis_dict_rehash(redis_dict, 1)


def redis_dict_rehash(redis_dict: RedisDict, n):
    pass


def redis_dict_resize(redis_dict: RedisDict):
    """
    缩小hash表的节点数量
    :param redis_dict:
    :return:
    """
    if not dict_can_resize or redis_dict_is_rehashing(redis_dict):
        return DICT_ERR
    minimal = redis_dict.ht[0].used
    # 计算让比率接近 1：1 所需要的最少节点数量
    if minimal < DICT_HT_INITIAL_SIZE:
        minimal = DICT_HT_INITIAL_SIZE
    return redis_dict_expand(redis_dict, minimal)


def redis_dict_expand(redis_dict: RedisDict, size):
    """
    hash表的扩容操作
    :param redis_dict:
    :param size:
    :return:
    """
    ht = DictHt()
    if redis_dict_is_rehashing(redis_dict) or redis_dict.ht[0].used > size:
        # rehash 或者 已经使用的节点大于 size 无法进行扩容操作
        return DICT_ERR
    realise_size = redis_dict_next_power(size)
    ht.size = realise_size
    ht.used = 0
    ht.sizemask = ht.size - 1
    ht.table = [RedisDictEntry() for _ in range(ht.size)]
    if redis_dict.ht[0].used == 0:
        # 初始化操作
        redis_dict.ht[0] = ht
        return DICT_OK
    # 进行到该处, 说明是rehash操作
    redis_dict.ht[1] = ht
    redis_dict.rehashidx = 0
    return DICT_OK


def redis_dict_next_power(size: int) -> int:
    """
    获取hash表的扩容大小, 默认以2的倍速进行扩容 2 ** n
    :param size:
    :return:
    """
    if size > LONG_MAX:
        return LONG_MAX
    i = DICT_HT_INITIAL_SIZE
    while 1:
        if i >= size:
            return i
        i *= 2


def redis_dict_is_rehashing(redis_dict: RedisDict):
    """
    rehashidx = -1, 表示字典没有进行rehash操作, 否则表示字典在 rehash中
    :param redis_dict:
    :return:
    """
    return redis_dict.rehashidx != -1
