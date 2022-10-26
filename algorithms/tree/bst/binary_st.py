from abc import ABC

from algorithms.search_st.abs_st import AbsST


class TreeNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None


class BinaryTreeST(AbsST, ABC):
    def __init__(self):
        self.root: TreeNode = None

    def put(self, key, val):
        self.root = self.recur_put(self.root, key, val)

    def recur_put(self, node: TreeNode, key, val) -> TreeNode:
        # 查找Key，如果找到就更新Key值，否则就插入一个新的Key
        if node is None:
            return TreeNode(key, val)
        if key == node.key:
            node.val = val
        elif key < node.key:
            node.left = self.recur_put(node.left, key, val)
        else:
            node.right = self.recur_put(node.right, key, val)
        return node

    def get(self, key):
        return self.recur_get(key, self.root)

    def recur_get(self, key, node: TreeNode):
        if node is None:
            return None
        if key == node.key:
            return node.val
        elif key < node.key:
            return self.recur_get(key, node.left)
        else:
            return self.recur_get(key, node.right)

    def delete(self, key):
        self.root = self.recur_delete(self.root, key)

    def recur_delete(self, node: TreeNode, key):
        # 如果树中，存在该Key节点，删除该节点，最后返回该子树
        if node is None:
            return None
        if key == node.key:
            if node.left:
                # 当前节点的左节点 -> 最右节点
                left_right_most = node.left
                while left_right_most.right:
                    left_right_most = left_right_most.right
                left_right_most.right = node.right
                return node.left
            else:
                return node.right
        elif key < node.key:
            node.left = self.recur_delete(node.left, key)
        else:
            node.right = self.recur_delete(node.right, key)
        return node

    def keys(self) -> list:
        if not self.root:
            return []

        result = []
        self.recur_keys(self.root, result)
        return result

    def recur_keys(self, node: TreeNode, all_keys: list):
        if node:
            if node.left:
                self.recur_keys(node.left, all_keys)
            all_keys.append(node.key)
            if node.right:
                self.recur_keys(node.right, all_keys)

    def size(self):
        return self.recur_size(self.root)

    def recur_size(self, node: TreeNode):
        if not node:
            return 0
        return self.recur_size(node.left) + self.recur_size(node.right) + 1

    def min_key(self):
        if not self.root:
            return None
        tree_most_left = self.root
        while tree_most_left.left:
            tree_most_left = tree_most_left.left
        return tree_most_left.val

    def max_key(self):
        if not self.root:
            return None
        tree_most_right = self.root
        while tree_most_right.right:
            tree_most_right = tree_most_right.right
        return tree_most_right.val

    def select(self, idx):
        tree_node = self.recur_select(self.root, idx)
        if tree_node:
            return tree_node.val
        return None

    def recur_select(self, node: TreeNode, idx):
        if node is None:
            return None
        node_size = self.recur_size(node.left)
        if node_size == idx:
            return node
        elif node_size < idx:
            return self.recur_select(node.right, idx - (node_size + 1))
        else:
            return self.recur_select(node.left, idx)

    def rank(self, key):
        if not self.root:
            return 0
        return self.recur_rank(self.root, key)

    def recur_rank(self, node: TreeNode, key):
        if node is None:
            return 0
        if key == node.key:
            return self.recur_size(node)
        elif key < node.key:
            return self.recur_rank(node.left, key)
        else:
            return self.recur_size(node.left) + 1 + self.recur_rank(node.right, key)

    def is_empty(self) -> bool:
        return self.size() == 0

    def contains(self, item) -> bool:
        return item in self.keys()


if __name__ == '__main__':
    from random import shuffle

    bs_tree = BinaryTreeST()
    test_keys = list(range(0, 100))
    shuffle(test_keys)
    for s in test_keys:
        bs_tree.put(s, s)
    assert bs_tree.contains(56)
    assert not bs_tree.contains(103)
    assert bs_tree.size() == 100
    assert bs_tree.min_key() == 0
    assert bs_tree.max_key() == 99
    assert bs_tree.select(98) == 98
    assert bs_tree.rank(56.3) == 57

    bs_tree.delete(47)
    assert bs_tree.size() == 99
    assert not bs_tree.contains(47)
    print(bs_tree.keys())
