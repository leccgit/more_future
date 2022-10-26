from copy import deepcopy

DICT_OK = 0  # hash表执行操作成功
DICT_ERR = 1  # hash表执行操作失败
dict_can_resize = 1  # hash表能执行扩容操作
LONG_MAX = 10241024  # 定义hash表的最大值
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
        return "Node(%s,%s)" % (self.key, self.value)


class DictIterator:
    """
     如果 safe 属性的值为 1 ,那么在迭代进行的过程中,
     程序仍然可以执行 dictAdd 、 dictFind 和其他函数,对字典进行修改。
     如果 safe 不为 1 ,那么程序只会调用 dictNext 对字典进行迭代,
     而不对字典进行修改。
    """
    __slots__ = ('d', 'table', 'index', 'safe', 'entry', 'nextEntry')

    def __init__(self):
        self.d = None  # 被迭代的字典
        self.table = None  # 正在被迭代的哈希表号码,值可以是 0 或 1 。
        self.index = None  # 迭代器当前所指向的哈希表索引位置
        self.safe = None  # 标识这个迭代器是否安全
        self.entry = None  # 当前迭代到的节点的指针
        # 当前迭代节点的下一个节点
        # 因为在安全迭代器运作时, entry 所指向的节点可能会被修改,
        # 所以需要一个额外的指针来保存下一节点的位置,
        # 从而防止指针丢失
        self.nextEntry = None


class DictHt:
    """ hash表中的hash table """
    __slots__ = ('table', 'size', 'sizemask', 'used')

    def __init__(self):
        self.table = None  # 哈希表数组 内部保存的是 RedisDictEntry节点
        self.size = 0  # 哈希表大小
        self.sizemask = 0  # 哈希表大小掩码,用于计算索引值, 总是等于 size - 1
        self.used = 0  # 该哈希表已有节点的数量

    def __repr__(self):
        return """
    size:{}
    used:{}
    sizemark:{}
    table:{}
        """.format(self.size, self.used, self.sizemask, self._fluent_table())

    def _fluent_table(self):
        if not self.table:
            return []
        result = []
        for cur_entry in self.table:
            t_node = []
            while cur_entry:
                t_node.append(str(cur_entry))
                cur_entry = cur_entry.next
            result.append(t_node)
        return result


class RedisDict:
    __slots__ = ('ht', 'type', 'privdata', 'rehashidx', 'iterators')

    def __init__(self):
        self.ht = [DictHt(), DictHt()]  # 哈希表
        self.type = None  # 设置类型特定函数
        self.privdata = None  # 私有数据
        self.rehashidx = -1  # rehash索引, 当rehash不在进行时,值为 -1
        self.iterators = 0  # 目前正在运行的安全迭代器的数量

    def __repr__(self):
        return 'H0:{}\nH1:{}'.format(str(self.ht[0]), str(self.ht[1]))


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


def redis_dict_init(redis_dict: RedisDict, data_type, privDataPtr):
    """
    初始化redis的字典
    :param redis_dict:
    :param data_type: 类型
    :param privDataPtr: 私有数据
    :return:
    """
    redis_dict_reset(redis_dict.ht[0])
    redis_dict_reset(redis_dict.ht[1])
    redis_dict.type = data_type
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


def redis_dict_expand(redis_dict: RedisDict, size):
    """
    hash表的初始化扩容操作
    T = O(N)
    创建一个新的哈希表,并根据字典的情况,选择以下其中一个动作来进行:
        1) 如果字典的 0 号哈希表为空,那么将新哈希表设置为 0 号哈希表
        2) 如果字典的 0 号哈希表非空,那么将新哈希表设置为 1 号哈希表,
           并打开字典的 rehash 标识,使得程序可以开始对字典进行 rehash
        size 参数不够大,或者 rehash 已经在进行时,返回 DICT_ERR.
        成功创建 0 号哈希表,或者 1 号哈希表时,返回 DICT_OK.
    :param redis_dict:
    :param size:
    :return:
    """
    real_size = redis_dict_next_power(size)
    if redis_dict_is_rehashing(redis_dict) or redis_dict.ht[0].used > size:
        # 正在rehash中, 则不重复进行扩容操作
        # 扩容后, 新hash表的大小, 不能小于原来已经使用的大小
        return DICT_ERR
    ht = DictHt()
    ht.used = 0
    ht.size = real_size
    ht.sizemask = ht.size - 1
    ht.table = [None for _ in range(ht.size)]
    if redis_dict.ht[0].used == 0:
        # hash表进行初始化, 所进行的扩容操作
        redis_dict.ht[0] = ht
        return DICT_OK
    # 正在rehash中, 只对1表进行rehash操作
    redis_dict.ht[1] = ht
    redis_dict.rehashidx = 0
    return DICT_OK


def redis_dict_rehash(redis_dict: RedisDict, n):
    """
    T = O(N)
    注意，每步rehash都是以一个哈希表索引(桶)作为单位的, 一个桶里可能会有多个节点
    被 rehash 的桶里的所有节点都会被移动到新哈希表
    执行n步的渐进式rehash操作
    :param redis_dict:
    :param n: 进行rehash的次数
    :return:
        0: 表示所有键都已经迁移完毕
        1: 表示仍有键需要从 0 号哈希表移动到 1 号哈希表
    """
    if not redis_dict_is_rehashing(redis_dict):
        return 0
    while n:
        if redis_dict.ht[0].used == 0:
            # 0号hash表的使用数量为0,表示迁移完毕,rehash结束
            redis_dict.ht[0] = deepcopy(redis_dict.ht[1])  # 由于python使用的是引用, 所以在该处需要进行深copy
            redis_dict_reset(redis_dict.ht[1])
            redis_dict.rehashidx = -1  # 关闭rehash的标志位
            return 0
        while redis_dict.ht[0].table[redis_dict.rehashidx] is None:
            # 当前节点为空
            redis_dict.rehashidx += 1
        # 指向链表的头节点
        current_entry = redis_dict.ht[0].table[redis_dict.rehashidx]
        while current_entry:
            next_entry = current_entry.next  # 保存下一节点的引用
            # 向hash Table中插入指定的节点
            insert_index = dict_hash_key(current_entry.key) % redis_dict.ht[1].sizemask
            current_entry.next = redis_dict.ht[1].table[insert_index]
            redis_dict.ht[1].table[insert_index] = current_entry
            # 更新节点使用次数
            redis_dict.ht[0].used -= 1
            redis_dict.ht[1].used += 1
            current_entry = next_entry
        # 更新0表中的该位置参数
        redis_dict.ht[0].table[redis_dict.rehashidx] = None
        redis_dict.rehashidx += 1
        n -= 1
    return 1


def redis_dict_add(redis_dict: RedisDict, key, value):
    """

    :param redis_dict:
    :param key:
    :param value:
    :return:
    """
    add_entry = redis_dict_add_raw(redis_dict, key)
    if add_entry is None:
        return DICT_ERR
    add_entry.value = value
    return DICT_OK


def redis_dict_add_raw(redis_dict: RedisDict, key) -> RedisDictEntry or None:
    """
    像redis的dict中, 插入一个原始的节点
    :param redis_dict:
    :param key:
    :return:
        None: if key in redis_dict
        entry: if key not in redis_dict
    """
    if redis_dict_is_rehashing(redis_dict):
        # 取值的时候, 需要进行单步的rehash操作
        redis_dict_rehash_step(redis_dict)
    # 查找索引
    key_index = redis_dict_key_index(redis_dict, key)
    if key_index == -1:
        return None
    # 根据哈希表中的rehash state选择将要插入的hash表
    ht = redis_dict.ht[1] if redis_dict_is_rehashing(redis_dict) else redis_dict.ht[0]
    dict_entry = RedisDictEntry()
    dict_entry.key = key
    dict_entry.next = ht.table[key_index]
    ht.table[key_index] = dict_entry
    ht.used += 1
    return dict_entry


def redis_dict_replace(redis_dict: RedisDict, key, val):
    """
    如果键值对为全新添加，那么返回 1
    如果键值对是通过对原有的键值对更新得来的，那么返回 0
    :param redis_dict:
    :param key:
    :param val:
    :return:
    """
    if redis_dict_add(redis_dict, key, val) == DICT_OK:
        # 尝试直接将键值对添加到字典
        # 如果键 key 不存在的话，添加会成功
        return 1
    dict_entry = redis_dict_find(redis_dict, key)
    dict_entry.value = val
    return 0


def redis_dict_replace_raw(redis_dict: RedisDict, key):
    """
    根据, key是否存在于 redis_dict执行以下操作
    1: 存在于redis_dict, 则直接返回该节点
    2: 将该key添加到redis_dict中
    :param redis_dict:
    :param key:
    :return:
    """
    key_entry = redis_dict_find(redis_dict, key)
    if key_entry:
        return key_entry
    return redis_dict_add_raw(redis_dict, key)


def redis_dict_find(redis_dict: RedisDict, key) -> RedisDictEntry or None:
    """
    if key not in redis_dict:
        return None
    :param redis_dict:
    :param key:
    :return:
    """
    if redis_dict.ht[0].size == 0:
        return None
    if redis_dict_is_rehashing(redis_dict):
        redis_dict_rehash_step(redis_dict)
    key_hash = dict_hash_key(key)
    for i in range(2):
        key_index = key_hash % redis_dict.ht[i].sizemask
        he = redis_dict.ht[i].table[key_index]
        while he:
            if he.key == key:
                return he
            he = he.next
        if not redis_dict_is_rehashing(redis_dict):
            # 如果, hash表处于rehash中, 则需要检查表1
            break
    return None


def redis_dict_generic_delete(redis_dict: RedisDict, key):
    """
    查找并删除包含给定键的节点
    找到并成功删除返回 DICT_OK ，没找到则返回 DICT_ERR
    :param redis_dict:
    :param key:
    :return:
    """
    if redis_dict.ht[0].size == 0:
        return None
    if redis_dict_is_rehashing(redis_dict):
        redis_dict_rehash_step(redis_dict)
    key_hash = dict_hash_key(key)
    for i in range(1):
        delete_index = key_hash % redis_dict.ht[i].sizemask
        he = redis_dict.ht[i].table[delete_index]
        pre_node = None
        while he:
            if he.key == key:
                # 在链表中, 删除该节点
                if pre_node is None:
                    redis_dict.ht[i].table[delete_index] = he.next
                else:
                    pre_node.next = he.next
                redis_dict.ht[i].used -= 1
                return DICT_OK
            else:
                pre_node = he
                he = he.next
        if not redis_dict_is_rehashing(redis_dict):
            break
    return DICT_ERR


def redis_dict_key_index(redis_dict: RedisDict, key):
    """
    获取 key在redis_dict中的hash表索引
    没有获取到,则返回-1
    :param redis_dict:
    :param key:
    :return:
    """
    if redis_dict_expand_if_needed(redis_dict) == DICT_ERR:
        return -1
    key_hash = dict_hash_key(key)
    key_index = -1
    for i in range(2):
        key_index = key_hash % redis_dict.ht[i].sizemask
        he = redis_dict.ht[i].table[key_index]

        while he:
            if he.key == key:
                return -1
            he = he.next
        if not redis_dict_is_rehashing(redis_dict):
            # 如果, redis_dict不处于rehash阶段, 那么检查表0已经足够
            break
    return key_index


def redis_dict_expand_if_needed(redis_dict: RedisDict):
    """
    根据需要,初始化字典(的哈希表),或者对字典(的现有哈希表)进行扩展
    :param redis_dict:
    :return:
    """
    if redis_dict_is_rehashing(redis_dict):
        return DICT_OK
    if redis_dict.ht[0].size == 0:
        return redis_dict_expand(redis_dict, DICT_HT_INITIAL_SIZE)
    # 一下条件为真的时候, 对字典进行扩展
    # 字典已使用的大小和字典的容量比例为1:1
    #    1. dict_can_resize为真
    #    2. 已经使用的节点, 和字典大小间的比率超过 dict_force_resize_ratio
    if redis_dict.ht[0].used >= redis_dict.ht[0].size and (
            dict_can_resize or
            redis_dict.ht[0].used / redis_dict.ht[0].size > dict_force_resize_ratio
    ):
        return redis_dict_expand(redis_dict, redis_dict.ht[0].used * 2)
    return DICT_OK


def redis_dict_rehash_step(redis_dict: RedisDict):
    """
    同时跌的的数量为0的时候, 进行单步的rehash操作
    :param redis_dict:
    :return:
    """
    if redis_dict.iterators == 0:
        redis_dict_rehash(redis_dict, 1)


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


if __name__ == '__main__':
    test_redis_dict = redis_dict_create('test', [])

    redis_dict_add(test_redis_dict, 'name', 'leichao')
    redis_dict_add(test_redis_dict, 'a', '1')
    redis_dict_add(test_redis_dict, 'b', '2')
    redis_dict_add(test_redis_dict, 'c', '3')
    redis_dict_add(test_redis_dict, 'd', '4')
    redis_dict_add(test_redis_dict, 'e', '5')
    redis_dict_add(test_redis_dict, 'f', '6')
    redis_dict_add(test_redis_dict, 'g', '7')
    assert redis_dict_find(test_redis_dict, 'g').value == '7'
    assert redis_dict_generic_delete(test_redis_dict, 'a') == DICT_OK
