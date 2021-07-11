"""
    简单lru的实现:
    缓存是一种将定量数据保存以备迎合后续获取需求的处理方式，旨在加快数据获取的速度。
    数据的生成过程可能需要经过计算，规整，远程获取等操作，如果是同一份数据需要多次使用，每次都重新生成会大大浪费时间。
    所以，如果将计算或者远程请求等操作获得的数据缓存下来，会加快后续的数据获取需求。
"""


class AbsLru(object):
    def set(self, key, value):
        raise NotImplemented

    def get(self, key):
        raise NotImplemented

    def has(self, key):
        raise NotImplemented

    def keys(self):
        raise NotImplemented

    def values(self):
        raise NotImplemented

    def size(self):
        raise NotImplemented


class Node(object):
    __slots__ = ("node", "value", "next_node")

    def __init__(self, node_key, node_value, next_node=None):
        self.node = node_key
        self.value = node_value
        self.next_node = next_node


class LinkList(object):
    __slots__ = ("heard", "_size", "_last_node")

    def __init__(self):
        self.heard = Node(None, None, None)
        self._size = 0
        self._last_node = None  # 尾节点

    def get_node(self, node_key):
        """
        获取节点值, 查不到的key 也默认返回None
        该处会存在混淆, 因为实际使用, value也有可能设置为None
        :param node_key:
        :return:
        """
        travel_heard = self.heard.next_node
        while travel_heard and travel_heard.node != node_key:
            travel_heard = travel_heard.next_node
        if travel_heard is not None:
            return travel_heard.value
        return None

    def has_node(self, node_key) -> bool:
        """
        判断节点是否存在
        :param node_key:
        :return:
        """
        travel_heard = self.heard.next_node
        while travel_heard and travel_heard.node != node_key:
            travel_heard = travel_heard.next_node
        if travel_heard is not None:
            return True
        return False

    def del_node(self, node_key):
        """
        删除节点, 这里使用快慢指针
        :param node_key:
        :return:
        """
        slow_heard = self.heard
        travel_heard = self.heard.next_node
        while travel_heard and travel_heard.node != node_key:
            travel_heard = travel_heard.next_node
            slow_heard = slow_heard.next_node
        if travel_heard is not None:
            if node_key == self._last_node:
                # 删除的为尾节点, 则尾节点发生变化
                self._last_node = slow_heard.node
            slow_heard.next_node = travel_heard.next_node
            self._size -= 1
            return travel_heard.value

    def del_last_node(self):
        """
        删尾节点
        :return:
        """
        self.del_node(self._last_node)

    def add_node(self, node_key, node_value):
        """
        追加节点, 头插法
        :param node_key:
        :param node_value:
        :return:
        """
        travel_heard = self.heard
        new_node = Node(node_key, node_value)
        if travel_heard.next_node is None:
            # 头节点为空
            travel_heard.next_node = new_node
        else:
            new_node.next_node = self.heard.next_node
            self.heard.next_node = new_node
        self._size += 1

    def node_size(self):
        return self._size

    def __repr__(self):
        print_repr = ["heard"]
        travel_heard = self.heard.next_node
        while travel_heard:
            print_repr.append("{" + '{} : {}'.format(travel_heard.node, travel_heard.value) + "}")
            travel_heard = travel_heard.next_node
        return ' <- '.join(print_repr) + ' <- None'


class QuickLru(AbsLru):
    __slots__ = ("max_size", "_keys", "_values")

    def __init__(self, max_size=10):
        self.max_size = max_size
        self.link_list = LinkList()

    def set(self, key, value):
        if self.link_list.has_node(key):
            self.link_list.del_node(key)
            self.link_list.add_node(key, value)
        else:
            if self.is_full():
                self.link_list.del_last_node()  # 删除尾节点
            self.link_list.add_node(key, value)

    def get(self, key):
        if self.link_list.has_node(key):
            node_value = self.link_list.del_node(key)
            self.link_list.add_node(key, node_value)
            return node_value
        else:
            return None

    def is_full(self) -> bool:
        return self.link_list.node_size() >= self.max_size

    def has(self, key) -> bool:
        return self.link_list.has_node(key)

    def size(self) -> int:
        return self.link_list.node_size()

    def __repr__(self):
        return str(self.link_list)


if __name__ == '__main__':
    lru = QuickLru(3)
    lru.set('🦄', '🌈')
    lru.set('🦄🦄', '🌈🌈')
    lru.set('🦄🦄🦄', '🌈🌈🌈')
    lru.set('🦄🦄🦄', '🦄🦄🦄')
    print(lru)
