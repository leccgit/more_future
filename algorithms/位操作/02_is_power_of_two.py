"""
一个数，如果是2的指数，那么它的二进制表示，只有一个1
"""


def is_power_of_two(n) -> bool:
    if n <= 0:
        return False
    return n & (n - 1) == 0


if __name__ == '__main__':
    assert is_power_of_two(2) is True
    assert is_power_of_two(8) is True
    assert is_power_of_two(7) is False
    assert is_power_of_two(-7) is False
