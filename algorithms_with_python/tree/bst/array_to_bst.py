class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None


def array_to_bst(nums: list) -> TreeNode or None:
    if not nums:
        return
    mid = len(nums) // 2
    tree_node = TreeNode(nums[mid])
    tree_node.left = array_to_bst(nums[:mid])
    tree_node.right = array_to_bst(nums[mid + 1:])
    return tree_node
