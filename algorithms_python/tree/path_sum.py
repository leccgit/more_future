"""
Given a binary tree and a sum, determine if the tree has a root-to-leaf
path such that adding up all the values along the path equals the given sum.

For example:
Given the below binary tree and sum = 22,
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \      \
        7    2      1
return true, as there exist a root-to-leaf path 5->4->11->2 which sum is 22.
"""
from algorithms_python.tree.tree_node import TreeNode


def path_sum(root: TreeNode, target_sum) -> bool:
    if root is None:
        return False
    if root.left is None and root.right is None and root.val == target_sum:
        return True
    target_sum -= root.val
    return path_sum(root.left, target_sum) or path_sum(root.right, target_sum)


# 类似 min_tree or max_tree的实现逻辑
def path_sum_2(root: TreeNode, target_sum) -> bool:
    if root is None:
        return False
    travel_tree = [(root, target_sum)]
    while travel_tree:
        new_travel = []
        for node, code_sum in travel_tree:
            if node.left is None and node.right is None and node.val == code_sum:
                return True
            if node.left is not None:
                new_travel.append((node.left, code_sum - node.val))
            if node.right is not None:
                new_travel.append((node.right, code_sum - node.val))
        travel_tree = new_travel
    return False


def path_sum_3(root: TreeNode, target_sum) -> bool:
    if root is None:
        return False
    tree_stack = [(root, target_sum)]
    while tree_stack:
        node, code_sum = tree_stack.pop()
        if node.left is None and node.right is None:
            if node.val == code_sum:
                return True
        if node.left is not None:
            tree_stack.append((node.left, code_sum - node.val))
        if node.right is not None:
            tree_stack.append((node.right, code_sum - node.val))
    return False


if __name__ == '__main__':
    pa_tree = TreeNode(5)
    pa_tree.left = TreeNode(4)
    pa_tree.right = TreeNode(8)

    pa_tree.left.left = TreeNode(11)
    pa_tree.left.left.left = TreeNode(7)
    pa_tree.left.left.right = TreeNode(2)

    pa_tree.right.left = TreeNode(13)
    pa_tree.right.right = TreeNode(4)

    pa_tree.right.right.right = TreeNode(1)

    print(path_sum(pa_tree, 22))
    print(path_sum_2(pa_tree, 22))
    print(path_sum_3(pa_tree,22))