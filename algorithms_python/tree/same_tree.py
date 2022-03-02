from algorithms_python.tree.tree_node import TreeNode


def is_same_tree(q: TreeNode, p: TreeNode) -> bool:
    if q is None and p is None:
        return True
    if q is not None and p is not None and q.val == p.val:
        return is_same_tree(q.left, p.left) and is_same_tree(q.right, p.right)
    return False
