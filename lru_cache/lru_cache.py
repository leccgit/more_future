class Node(object):
    __slots__ = ("results", "next_node", "pre_node")

    def __init__(self, results, next_node=None, pre_node=None):
        self.results = results
        self.next_node = next_node  # 后置节点
        self.pre_node = pre_node  # 前置节点

    def __repr__(self):
        return "<node:{}>".format(self.results)


class LinkedList(object):

    def __init__(self):
        self.head = self.tail = None
        self.size = 0

    def move_to_front(self, node: Node):
        if node == self.tail or node == self.head:
            # 头尾节点,就不做处理了
            pass
        else:
            node.next_node.pre_node = node.pre_node
            node.pre_node.next_node = node.next_node
            self.append_to_front(node)

    def append_to_front(self, node):
        if self.size == 0:
            self.head = self.tail = node
            self.head.pre_node = self.tail.next_node = None
        else:
            node.pre_node = None
            node.next_node = self.head
            self.head.pre_node = node
            self.head = node
        self.size += 1

    def remove_from_tail(self):
        if self.tail.pre_node != self.head:
            self.tail = self.tail.pre_node
            self.tail.next_node = None

    def move_to_tail(self, node: Node):
        if self.size == 0:
            self.head = self.tail = node
            self.head.pre_node = self.tail.next_node = None
        else:
            node.next_node = None
            node.pre_node = self.tail
            self.tail.next_node = node
            self.tail = node
        self.size += 1


class Cache(object):

    def __init__(self, MAX_SIZE):
        self.MAX_SIZE = MAX_SIZE
        self.size = 0
        self.lookup = {}  # key: query, value: node
        self.linked_list = LinkedList()

    def get(self, query):
        """Get the stored query result from the cache.

        Accessing a node updates its position to the front of the LRU list.
        """
        node = self.lookup.get(query)
        if node is None:
            return None
        self.linked_list.move_to_front(node)
        return node.results

    def set(self, results, query):
        """Set the result for the given query key in the cache.

        When updating an entry, updates its position to the front of the LRU list.
        If the entry is new and the cache is at capacity, removes the oldest entry
        before the new entry is added.
        """
        node = self.lookup.get(query)
        if node is not None:
            # Key exists in cache, update the value
            node.results = results
            self.linked_list.move_to_front(node)
        else:
            # Key does not exist in cache
            if self.size == self.MAX_SIZE:
                # Remove the oldest entry from the linked list and lookup
                self.lookup.pop(self.linked_list.tail.results, None)
                self.linked_list.remove_from_tail()
            else:
                self.size += 1
            # Add the new key and value
            new_node = Node(results)
            self.linked_list.append_to_front(new_node)
            self.lookup[query] = new_node


if __name__ == '__main__':
    lru = Cache(3)
    lru.set('🌈', '🦄')
    lru.set('🌈🌈', '🦄🦄')
    lru.set('🌈🌈🌈', '🦄🦄🦄')
    lru.set('🦄🦄🦄', '🦄🦄🦄')
    print(lru.get('🦄'))

    print(lru.lookup)
