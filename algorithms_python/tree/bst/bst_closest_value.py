import unittest

from algorithms_python.tree.tree_node import TreeNode

"""
    5
   / \
  3   6
 / \   \
2   4   7
"""


def bst_closest_value(root: TreeNode, target):
    if not root:
        return None
    closest_value, closest_node = target, root
    stack = [root]
    while stack:
        node = stack.pop()
        if abs(node.val - target) <= closest_value:
            closest_node = node
            closest_value = abs(node.val - target)

        if node.left:
            if abs(node.left.val - target) < closest_value:
                stack.append(node.left)
        if node.right:
            if abs(node.right.val - target) < closest_value:
                stack.append(node.right)
    return closest_node.val


class TestSuite(unittest.TestCase):
    def setUp(self):
        self.tree = TreeNode(5)
        self.tree.left = TreeNode(3)
        self.tree.right = TreeNode(6)

        self.tree.left.left = TreeNode(2)
        self.tree.left.right = TreeNode(4)

        self.tree.right.right = TreeNode(7)

    def test_count_left_node(self):
        print(bst_closest_value(self.tree, 3.2))
        self.assertEqual(3, bst_closest_value(self.tree, 3.2))


if __name__ == '__main__':
    unittest.main()
