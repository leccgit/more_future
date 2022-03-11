import unittest

from algorithms_python.tree.bst.bst import BST
from algorithms_python.tree.tree_node import TreeNode


def bst_height(root: TreeNode):
    if not root:
        return 0
    return 1 + max(bst_height(root.left), bst_height(root.right))


def bst_height_2(root: TreeNode):
    if not root:
        return 0
    max_child_height = 0
    if root.left:
        max_child_height = bst_height_2(root.left)
    if root.right:
        max_child_height = max(max_child_height, bst_height_2(root.right))
    return 1 + max_child_height


"""
    The tree is created for testing:

                    9
                 /      \
               6         12
              / \       /   \
            3     8   10      15
                 /              \
                7                18

    count_left_node = 4

"""


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.tree = BST()
        self.tree.insert(9)
        self.tree.insert(6)
        self.tree.insert(12)
        self.tree.insert(3)
        self.tree.insert(8)
        self.tree.insert(10)
        self.tree.insert(15)
        self.tree.insert(7)
        self.tree.insert(18)

    def test_height(self):
        self.assertEqual(4, bst_height(self.tree.root))
        self.assertEqual(4, bst_height_2(self.tree.root))


if __name__ == '__main__':
    unittest.main()
