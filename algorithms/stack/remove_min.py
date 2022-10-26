"""
删除栈中的最小元素，与之相对的是删除栈中的指定元素
栈的顺序恢复，可以使用另一个栈临时存储 栈中pop()的数据
"""


def remove_min(stack) -> list:
    if not stack:
        return stack
    reverse_stack = []  # 临时存储栈中的元素, 与原来的顺序相反
    # 查找stack最小值
    min_val = stack.pop()
    stack.append(min_val)
    for _ in range(len(stack)):
        val = stack.pop()
        if val < min_val:
            min_val = val
        reverse_stack.append(val)
    # 重键栈，同时删除最小元素
    for _ in range(len(reverse_stack)):
        num = reverse_stack.pop()
        if num != min_val:
            stack.append(num)
    return stack


if __name__ == '__main__':
    assert [] == remove_min([2])
    assert [2, 8, 3, 7, 3] == remove_min([2, 8, 3, -6, 7, 3])
    assert [4, 8, 7] == remove_min([4, 8, 3, 7, 3])
