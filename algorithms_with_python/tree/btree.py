# TODO: Btree的具体实现
class Node:
    def __init__(self):
        # self.is_leaf = is_leaf
        self.keys = []
        self.children = []

    def __repr__(self):
        return "<id_node: {0}>".format(self.keys)

    @property
    def is_leaf(self):
        return len(self.children) == 0


class BTree:
    def __init__(self, t=2):
        self.root = Node()

    def insert_key(self, key):
        pass

    def find(self, key):
        pass

    def remove_key(self, key):
        pass
