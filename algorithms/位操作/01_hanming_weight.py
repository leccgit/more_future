def hanming_weight(num) -> int:
    if num == 0:
        return 0
    if num < 0:
        num = abs(num)
    res = 0
    while num != 0:
        num = num & (num - 1)
        res += 1
    return res


if __name__ == '__main__':
    assert hanming_weight(2) == 1
    assert hanming_weight(8) == 1
    assert hanming_weight(7) == 3
    print(hanming_weight(-7), bin(-7))
    assert hanming_weight(-7) == 3
