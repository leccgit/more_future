# 从表头向表尾进行迭代
AL_START_HEAD = 0
# 从表尾到表头进行迭代
AL_START_TAIL = 1


class Node:
    def __init__(self, value, prev_node=None, next_node=None):
        self.value = value  # 节点的值
        self.prev_node = prev_node  # 前置节点
        self.next_node = next_node  # 后置节点

    def __repr__(self):
        return "[Node:{}, Value:{}]".format(id(self), self.value)


class ListIter:
    # 双端链表迭代器
    def __init__(self, iter_node: Node, direction):
        self.iter_node = iter_node
        self.direction = direction  # 迭代器的方向

    def __iter__(self):
        current = next(self)
        while current is not None:
            yield current
            current = next(self)

    def __next__(self):
        # 获取迭代器中, 当前迭代的节点
        current = self.iter_node
        if current:
            if self.direction == AL_START_HEAD:
                self.iter_node = current.next_node
            else:
                self.iter_node = current.prev_node
        return current


class ADLinkList:
    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def list_add_node_head(self, value):
        """ 插入头节点 """
        node = Node(value)
        if self.size == 0:
            self.head = self.tail = node
            self.head.prev_node = self.tail.next_node = None
        else:
            node.next_node = self.head
            self.head.prev_node = node
            self.head = node
        self.size += 1
        return self.head

    def list_add_node_tail(self, value):
        """ 插入尾节点 """
        node = Node(value)
        if self.size == 0:
            self.head = self.tail = node
            self.head.prev_node = self.tail.next_node = None
        else:
            node.prev_node = self.tail
            self.tail.next_node = node
            self.tail = node
        self.size += 1
        return self.head

    def list_insert_node(self, old_node: Node, value, after=True):
        """
        将当前节点, 默认插入制定节点之后
        :param old_node:
        :param value:
        :param after: bool
        :return:
        """
        node = Node(value)
        if after:
            # 将当前节点, 添加到指定节点之后
            node.prev_node = old_node
            node.next_node = old_node.next_node
            # 如果给定节点是尾节点, 更新尾节点值
            if old_node == self.tail:
                self.tail = node
        else:
            # 将当前节点, 添加到指定节点之间
            node.next_node = old_node
            node.prev_node = old_node.prev_node
            # 如果给定节点是头节点, 更新头节点值
            if old_node == self.head:
                self.head = node
        # 更新当前节点的头节点
        if node.prev_node is not None:
            node.prev_node.next_node = node
        # 更新当前节点的尾节点
        if node.next_node is not None:
            node.next_node.prev_node = node
        self.size += 1
        return self.head

    def list_del_node(self, node: Node):
        """
        删除链表中的指定节点, 如果指定节点不在链表中, 那么程序会异常
        节点的校验, 放在处理层上
        :param node:
        :return:
        """
        if node.prev_node:
            node.prev_node.next_node = node.next_node
        else:
            self.head = node.next_node
        if node.next_node:
            node.next_node.prev_node = node.prev_node
        else:
            self.tail = node.prev_node
        self.size -= 1

    def list_get_iterator(self, direction=AL_START_HEAD):
        """
        获取当前链表的迭代方向
        :param direction:
        :return:
        """
        assert direction in [AL_START_HEAD, AL_START_TAIL], 'direction value error!'
        if direction == AL_START_HEAD:
            cur_iterator = ListIter(self.head, direction)
        else:
            cur_iterator = ListIter(self.tail, direction)
        return cur_iterator

    def list_search_key(self, key):
        """
        在链表中查找, 目标key是否存在, 不存在则返回None
        :param key:
        :return:
        """
        for copy_node in self.list_get_iterator(AL_START_TAIL):
            # 在该处, 添加match, 则能使用正则匹配
            if copy_node.value == key:
                return copy_node
        return None

    def list_dump(self):
        # 复制链表, 从头节点进行复制
        copy = self.__class__()
        for copy_node in self.list_get_iterator(AL_START_TAIL):
            copy.list_add_node_tail(copy_node.value)
        return copy

    def list_index(self, index):
        assert type(index) == int
        if index < 0:
            index = (-index) - 1
            current_node = self.tail
            while current_node and index > 0:
                index -= 1
                current_node = current_node.prev_node
        else:
            current_node = self.head
            while current_node and index > 0:
                index -= 1
                current_node = current_node.next_node

        return current_node

    def list_rotate(self):
        tail_node = self.tail
        if self.size <= 0:
            return
        self.tail = self.tail.prev_node
        self.tail.next_node = None

        self.head.prev_node = tail_node
        tail_node.prev_node = None
        tail_node.next_node = self.head
        self.head = tail_node

    def __len__(self):
        return self.size

    def __repr__(self):
        return 'hear ' + ' <==> '.join(str(node) for node in list(self.list_get_iterator())) + ' <==> tail'


if __name__ == '__main__':
    ad_list = ADLinkList()
    assert len(ad_list) == 0
    ad_list.list_add_node_head(10)
    ad_list.list_add_node_head(15)
    assert len(ad_list) == 2
    ad_list.list_add_node_tail(30)

    ad_list.list_insert_node(ad_list.head, 8)
    assert len(ad_list) == 4

    # 复制链表
    new_link = ad_list.list_dump()
    assert new_link != ad_list
    assert ad_list.list_search_key(8) is not None
    assert ad_list.list_index(-3) == ad_list.list_index(1)
    print(ad_list)
    ad_list.list_rotate()
    print(ad_list)
