"""
    The tree is created for testing:

                    9
                 /      \
               6         12
              / \       /   \
            3     8   10      15
                 /              \
                7                18

    depth_sum = 1*9 + 2*(6+12) + 3*(3+8+10+15) + 4*(7+18)

"""
import unittest

from algorithms_with_python.tree.bst.bst import BST, Node


def depth_sum(root: Node, max_depth: int):
    if not root:
        return 0
    return recur_depth_sum(root, 1, max_depth)


def _recur_depth_sum(root: Node, depth: int, max_depth: int):
    if root is None or depth > max_depth:
        return 0
    return depth * root.data + recur_depth_sum(
        root.left, depth + 1, max_depth) + recur_depth_sum(root.right, depth + 1, max_depth)


def recur_depth_sum(root: Node, depth: int, max_depth: int):
    if root is None or depth > max_depth:
        return 0
    result = depth * root.data
    if root.left:
        result += recur_depth_sum(root.left, depth + 1, max_depth)
    if root.right:
        result += recur_depth_sum(root.right, depth + 1, max_depth)
    return result


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

    def test_depth_sum(self):
        self.assertEqual(253, depth_sum(self.tree.root, 4))


if __name__ == '__main__':
    unittest.main()
