"""
    简单lru的实现:
    缓存是一种将定量数据保存以备迎合后续获取需求的处理方式，旨在加快数据获取的速度。
    数据的生成过程可能需要经过计算，规整，远程获取等操作，如果是同一份数据需要多次使用，每次都重新生成会大大浪费时间。
    所以，如果将计算或者远程请求等操作获得的数据缓存下来，会加快后续的数据获取需求。
    使用双端链表实现, 可以避免单链表查询需要遍历整个链表的问题, 在该处增加了节点的缓存map
    类比: collection 中的 OrderDict的是实现, ps redis中的lru实现方式并不一致
"""
from collections import OrderedDict
from functools import lru_cache

lru_cache

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
    __slots__ = ("node", "value", "next_node", "pre_node")

    def __init__(self, node_key, node_value, pre_node=None, next_node=None):
        """

        :param node_key:
        :param node_value:
        :param pre_node: 前置节点
        :param next_node: 后置节点
        """
        self.node = node_key
        self.value = node_value
        self.pre_node = pre_node
        self.next_node = next_node

    def __repr__(self):
        return "{" + '{} : {}'.format(self.node, self.value) + "}"


class LinkList(object):
    __slots__ = ("heard", "tail", "link_cache")

    def __init__(self):
        self.link_cache = {}
        self.heard = Node(None, None, None)  # 头节点
        self.tail = Node(None, None, None)  # 尾节点
        # 建立头尾节点的关系
        self.heard.next_node = self.tail
        self.tail.pre_node = self.heard

    def get_node(self, node_key):
        """
        获取节点值, 查不到的key 也默认返回None
        该处会存在混淆, 因为实际使用, value也有可能设置为None
        :param node_key:
        :return:
        """
        node_item = self.link_cache[node_key]
        if not node_item:
            return -1
        self.move_to_head(node_item)
        return node_item

    def move_to_head(self, link_node: Node):
        """
        a --- b
        a --- c --- b
        :param link_node:
        :return:
        """

        self.del_node(link_node)
        self.add_node(link_node)

    def add_node(self, link_node: Node):
        """
        追加节点, 头插法
        :param link_node:
        :return:
        """
        self.link_cache[link_node.node] = link_node
        link_node.pre_node = self.heard
        link_node.next_node = self.heard.next_node

        # ps: 注意这个的顺序不能更改
        self.heard.next_node.pre_node = link_node
        self.heard.next_node = link_node

    def has_node(self, node_key) -> bool:
        """
        判断节点是否存在
        :param node_key:
        :return:
        """
        return node_key in self.link_cache

    def del_node(self, link_node: Node):
        """
        :param link_node:
        :return:
        """
        cache_node_pre = link_node.pre_node
        cache_node_next = link_node.next_node

        cache_node_pre.next_node = cache_node_next
        cache_node_next.pre_node = cache_node_pre
        del self.link_cache[link_node.node]

    def del_last_node(self):
        """
        剔除尾节点
        :return:
        """
        last_node = self.tail.pre_node
        self.del_node(last_node)

    def node_size(self):
        return len(self.link_cache)

    def __repr__(self):
        print_repr = ["heard"]
        travel_heard = self.heard.next_node
        while travel_heard and travel_heard.node:
            print_repr.append(str(self.link_cache[travel_heard.node]))
            travel_heard = travel_heard.next_node
        return ' <- '.join(print_repr) + ' <- tail'


class QuickLru(AbsLru):
    __slots__ = ("max_size", "_keys", "_values")

    def __init__(self, max_size=10):
        self.max_size = max_size
        self.link_list = LinkList()

    def set(self, key, value):
        if self.link_list.has_node(key):
            current_node = self.link_list.get_node(key)
            current_node.value = value
        else:
            if self.is_full():
                self.link_list.del_last_node()
            new_node = Node(key, value)
            self.link_list.add_node(new_node)

    def get(self, key):
        if self.link_list.has_node(key):
            current_node = self.link_list.get_node(key)
            return current_node.value
        else:
            return -1

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
    assert lru.get('🌈') == -1
    assert lru.get('🦄🦄') == '🌈🌈'

    print(lru)
