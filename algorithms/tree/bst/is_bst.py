import unittest

from algorithms.tree.bst.bst import BST, Node


def is_bst(root: Node) -> bool:
    if not root:
        return True
    if root.left:
        if root.data < root.left.data:
            return False
    if root.right:
        if root.data > root.right.data:
            return False
    return True and is_bst(root.left) and is_bst(root.right)


def is_bst_2(root: Node) -> bool:
    if not root:
        return True
    stack = [root]
    while stack:
        tree_node = stack.pop()
        if tree_node.left:
            if tree_node.data < tree_node.left.data:
                return False
            else:
                stack.append(tree_node.left)
        if tree_node.right:
            if tree_node.data > tree_node.right.data:
                return False
            else:
                stack.append(tree_node.right)
    return True


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.tree = BST()
        self.tree.insert(3)
        self.tree.insert(4)
        self.tree.insert(2)
        self.tree.insert(36)
        self.tree.insert(86)
        self.tree.insert(160)
        self.tree.insert(155)
        self.tree.insert(74)
        self.tree.insert(138)

    def test_is_bst(self):
        self.assertTrue(is_bst(self.tree.root))
        self.assertTrue(is_bst_2(self.tree.root))


if __name__ == '__main__':
    unittest.main()
