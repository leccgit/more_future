LONG_MAX = 1024 * 1024  # 定义hash表的最大值
DICT_HT_INITIAL_SIZE = 4  # 初始化哈希表的大小
dict_force_resize_ratio = 5  # 强制 rehash 的比率
dict_can_resize = 1
DICT_OK = 0
DICT_ERR = 1


def key_hash_function(key: str):
    """ key的hash值函数 """
    return abs(hash(key))


class RedisDictEntry:
    """ 字典中的节点 """

    def __init__(self, key, value=None, next_dictEntry=None):
        self.key = key
        self.value = value
        self.next = next_dictEntry

    def __repr__(self):
        return "<key={} value={}>".format(self.key, self.value)


class DictHt:
    """ hash表 """

    def __init__(self, size=0, sizemask=0, used=0):
        self.table = [None for _ in range(size)] if size != 0 else []  # 哈希表数组 内部保存的是 RedisDictEntry节点
        self.size = size  # 哈希表大小
        self.sizemask = sizemask  # 哈希表大小掩码，用于计算索引值, 总是等于 size - 1
        self.used = used  # 该哈希表已有节点的数量

    def hash(self, dict_entry: RedisDictEntry):
        return hash(dict_entry.key) % self.size


class RedisDict:
    """ 字典数据结构 """

    def __init__(self, type, privdata):
        self._dict_init(type, privdata)

    def _dict_init(self, type, privdata):
        """
        初始化hash表, 为避免内存浪费, 初始化的时候, 不对table进行 初始化大小操作
        :param type:
        :param privdata:
        :return:
        """
        self.dictht = [None, None]  # 哈希表
        self.dictht[0] = self._dict_ht_reset()
        self.dictht[1] = self._dict_ht_reset()
        self.type = type  # 设置类型特定函数
        self.privdata = privdata  # 私有数据

        self.rehashidx = -1  # rehash索引, 当rehash不在进行时，值为 -1
        self.iterators = 0  # 目前正在运行的安全迭代器的数量

    def dict_is_rehashing(self):
        return self.rehashidx != -1

    def dict_resize(self):
        """ 缩小hash表的大小 """
        if not dict_can_resize or self.dict_is_rehashing():
            # 关闭自动rehash 或者 字典正在 rehash中, 不进行缩小操作
            return DICT_ERR
        minimal = self.dictht[0].used
        if minimal < DICT_HT_INITIAL_SIZE:
            minimal = DICT_HT_INITIAL_SIZE
        return self.dict_expand(minimal)

    def dict_expand(self, size):
        """ 对hash表进行伸缩操作 """

        if self.dict_is_rehashing() or self.dictht[0].used > size:
            # dict正在rehash中或者 已经使用的节点大于 size, 不进行扩容操作
            return DICT_ERR
        next_size = self._dict_next_power(size)
        new_dict = DictHt(size=next_size, sizemask=next_size - 1, used=0)  # 新的hash表
        if not self.dictht[0].table:
            # 0号的hash表为空,则说明是一个初始化操作
            self.dictht[0] = new_dict
            return DICT_OK
        self.dictht[1] = new_dict
        self.rehashidx = 0  # 开启rehash标志, 让程序可以进行rehash操作
        return DICT_OK

    def dict_add(self, key, value):
        """
        向table中插入节点
        :param key:
        :param value:
        :return:
        """
        add_entry = self.dict_add_raw(key)
        if add_entry is None:
            return DICT_ERR
        add_entry.value = value
        return DICT_OK

    def dict_add_raw(self, key) -> RedisDictEntry or None:
        """
        向table中插入节点
        返回None,代表key已经存在table中,无法进行插入
        :param key:
        :return:
        """

        key_index = self._dict_key_index_if_can_add(key)
        if key_index == -1:
            return
        ht = self.dictht[1] if self.dict_is_rehashing() else self.dictht[0]
        new_dict_entry = RedisDictEntry(key)
        new_dict_entry.next = ht.table[key_index]
        ht.table[key_index] = new_dict_entry
        ht.used += 1
        return new_dict_entry

    def _dict_key_index_if_can_add(self, key) -> int:
        """
        如果, key存在hash表中, 默认返回-1, 否则返回其索引位置
        如果 字典正在 rehash中, 则默认返回 table[1]中的索引
        :param key:
        :return:
        """
        if self._dict_expand_if_needed() == DICT_ERR:
            return -1
        key_hash = key_hash_function(key)
        key_index = -1
        for i in range(2):
            key_index = key_hash % self.dictht[i].sizemask
            key_entry = self.dictht[i].table[key_index]  # 获取指定位置的头节点
            while key_entry:
                if key_entry.key == key:
                    return -1
                key_entry = key_entry.next

            if not self.dict_is_rehashing():
                # 不在rehash中, 只需要检查0表就够了
                # 否则, 一定是添加到1表中, 计算1表中的索引位置
                break
        return key_index

    def _dict_expand_if_needed(self):
        """
        字典的扩容操作
        :return:
        """
        if self.dict_is_rehashing():
            return DICT_OK
        if self.dictht[0].size == 0:
            # 初始化操作
            return self.dict_expand(DICT_HT_INITIAL_SIZE)
        if self.dictht[0].used >= self.dictht[0].size or (
                dict_can_resize
                or self.dictht[0].used / self.dictht[0].size >= 5):
            # 一下两个条件之一为真时，对字典进行扩展
            # 1）字典已使用节点数和字典大小之间的比率接近 1：1
            # 并且dict_can_resize为真
            # 2）已使用节点数和字典大小之间的比率超过 dict_force_resize_ratio
            return self.dict_expand(DICT_HT_INITIAL_SIZE)

        return DICT_OK

    def dict_rehash(self, n=100):
        """
        渐进式的rehash操作, 单次默认执行100次
        :param n:
        :return:
            返回 0 ,向调用者表示 rehash 已经完成
        """
        if not self.dict_is_rehashing():
            return 0
        while n > 0:
            if self.dictht[0].used == 0:
                # rehash结束, 更新节点的使用
                self.dictht[0] = self.dictht[1]
                self.dictht[1] = self._dict_ht_reset()
                self.rehashidx = -1  # 标志关闭rehash操作
                return 0
            while not self.dictht[0].table[self.rehashidx]:
                # 找到下一个非空的 entry节点
                self.rehashidx += 1
            # 找到非空entry链表的头节点
            cur_entry = self.dictht[0].table[self.rehashidx]
            while cur_entry:
                next_entry = cur_entry.next
                insert_index = key_hash_function(cur_entry.key) % self.dictht[1].sizemask

                cur_entry.next = self.dictht[1].table[insert_index]  # 在该处使用的是链表的头插法
                self.dictht[1].table[insert_index] = cur_entry

                self.dictht[0].used -= 1
                self.dictht[1].used += 1

                cur_entry = next_entry  # 下一个处理节点
            # 将刚迁移完的哈希表索引的指针设为空
            self.dictht[0].table[self.rehashidx] = None
            # rehash的索引前移
            self.rehashidx += 1
            n -= 1
        return 1

    def _dict_next_power(self, size):
        """ 根据size确定后续伸缩的Hash表大小 """
        if size > LONG_MAX:
            return LONG_MAX
        i = DICT_HT_INITIAL_SIZE
        while 1:
            if i >= size:
                return i
            i *= 2

    def _dict_ht_reset(self):
        """ 初始化hash表的节点 """
        return DictHt()

    def __repr__(self):
        all_entry = []
        for entry in self.dictht[0].table:
            tm = []
            while entry:
                tm.append(str(entry))
                entry = entry.next
            all_entry.append('[{}]'.format(' '.join(tm)))
        return ' '.join(all_entry)


def dict_disable_resize():
    """ 关闭自动 rehash """
    global dict_can_resize
    dict_can_resize = 0


def dict_enable_resize():
    """ 开启自动 rehash """
    global dict_can_resize
    dict_can_resize = 1


if __name__ == '__main__':
    current_dict = RedisDict('str', None)
    from random import choice, randint

    for i in range(20):
        key = choice('asdfghjklqwertyuiopzcvbn')
        print(key)
        current_dict.dict_add(key, randint(1, 100))
        print(current_dict)
    print(current_dict)
