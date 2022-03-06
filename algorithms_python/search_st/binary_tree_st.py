from abc import ABC
from typing import Iterator

from algorithms_python.search_st.abs_st import AbsST


class TreeNode:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.left = None
        self.right = None


def count_tree_nodes(tree_node: TreeNode) -> int:
    if tree_node is None:
        return 0
    return count_tree_nodes(tree_node.left) + count_tree_nodes(tree_node.right) + 1


class BinaryTreeST(AbsST, ABC):
    def __init__(self):
        self.root: TreeNode = None

    def put(self, key, val):
        self.root = self._put(self.root, key, val)

    def _put(self, node: TreeNode, key, val):
        if node is None:
            return TreeNode(key, val)
        if key < node.key:
            node.left = self._put(node, key, val)
        elif key > node.key:
            node.right = self._put(node, key, val)
        else:
            node.val = val

    def get(self, key):
        return self._get(key, self.root)

    def _get(self, key, node: TreeNode):
        if node is None:
            return None
        if key < node.key:
            return self._get(key, node.left)
        elif key > node.key:
            return self._get(key, node.right)
        else:
            return node.val

    def delete(self, key):
        self.put(key, None)

    def keys(self) -> Iterator:
        if not self.root:
            pass

    def _keys(self, node: TreeNode):
        if node:
            yield node.key
            self._keys(node.left)
            self._keys(node.right)

    def size(self):
        if self.root:
            return count_tree_nodes(self.root)
        return 0

    def is_empty(self) -> bool:
        return self.size() == 0

    def contains(self, item) -> bool:
        return item in list(self.keys())
