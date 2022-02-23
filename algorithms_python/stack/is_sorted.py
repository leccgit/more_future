def is_sorted(stack: list) -> bool:
    len_stack = len(stack)
    for _ in range(len_stack):
        if len(stack) == 0:
            break
        fi = stack.pop()
        if len(stack) == 0:
            break
        se = stack.pop()
        if fi < se:
            return False
        stack.append(se)
    return True


if __name__ == '__main__':
    assert is_sorted([6, 3, 5, 1, 2, 4]) is False
    assert is_sorted([1, 2, 3, 4, 5, 6]) is True
    assert is_sorted([3, 4, 7, 8, 5, 6]) is False
