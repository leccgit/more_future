from algorithms.tree.tree_node import TreeNode


def min_height(root) -> int:
    if not root:
        return 0
    tree_level = 0
    travel_lever = [root]
    while travel_lever:
        tree_level += 1
        new_travel = []
        for node in travel_lever:
            if node.left is None and node.right is None:
                return tree_level
            if node.left is not None:
                new_travel.append(node.left)
            if node.right is not None:
                new_travel.append(node.right)
        travel_lever = new_travel
    return tree_level


def print_tree(root):
    if root is not None:
        print(root.val)
        print_tree(root.left)
        print_tree(root.right)


if __name__ == '__main__':
    tree = TreeNode(10)
    tree.left = TreeNode(12)
    tree.right = TreeNode(15)
    tree.left.left = TreeNode(25)
    tree.left.left.right = TreeNode(100)
    tree.left.right = TreeNode(30)
    tree.right.left = TreeNode(36)

    height = min_height(tree)
    print_tree(tree)
    print("height:", height)
