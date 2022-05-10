"""
Given a binary tree and a sum, find all root-to-leaf
paths where each path's sum equals the given sum.

For example:
Given the below binary tree and sum = 22,
              5
             / \
            4   8
           /   / \
          11  13  4
         /  \    / \
        7    2  5   1
return
[
   [5,4,11,2],
   [5,8,4,5]
]
"""
from algorithms_with_python.tree.tree_node import TreeNode


def path_sum(root: TreeNode, target_sum) -> list:
    if root is None:
        return []
    result = []
    path_dfs(root, target_sum, [], result)
    return result


def path_dfs(root: TreeNode, target_sum, ls, rs):
    if root.left is None and root.right is None and root.val == target_sum:
        ls.append(root.val)
        rs.append(ls)
    if root.left is not None:
        path_dfs(root.left, target_sum - root.val, ls + [root.val], rs)
    if root.right is not None:
        path_dfs(root.right, target_sum - root.val, ls + [root.val], rs)


def path_sum_2(root: TreeNode, target_sum) -> list:
    if root is None:
        return []
    result = []
    travel_stack = [(root, target_sum, [])]
    while travel_stack:
        node, code_sum, ls = travel_stack.pop()
        if node.left is None and node.right is None and node.val == code_sum:
            ls.append(node.val)
            result.append(ls)
        if node.left is not None:
            travel_stack.append((node.left, code_sum - node.val, ls + [node.val]))
        if node.right is not None:
            travel_stack.append((node.right, code_sum - node.val, ls + [node.val]))
    return result


if __name__ == '__main__':
    pa_tree = TreeNode(5)
    pa_tree.left = TreeNode(4)
    pa_tree.right = TreeNode(8)

    pa_tree.left.left = TreeNode(11)
    pa_tree.left.left.left = TreeNode(7)
    pa_tree.left.left.right = TreeNode(2)

    pa_tree.right.left = TreeNode(13)
    pa_tree.right.right = TreeNode(4)

    pa_tree.right.right.left = TreeNode(5)
    pa_tree.right.right.right = TreeNode(1)

    print(path_sum(pa_tree, 22))
    print(path_sum_2(pa_tree, 22))
