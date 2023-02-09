"""
查找只出现一次的元素
但是，注意，如果出现一次的元素由多个的话，该操作就有问题
一个数和它本身做异或运算结果为 0，即 `a ^ a = 0`；一个数和 0 做异或运算的结果为它本身，即 `a ^ 0 = a`。

"""
from typing import List


def single_num(nums: List):
    res = 0
    for num in nums:
        res ^= num
    return res


if __name__ == '__main__':
    print(single_num([1, 2, 2, 3, 3, 4, 4]))
    print(single_num([2, 2, 3, 3, 4, 4, 6]))
    print(single_num([2, 2, 3, 3, 4, 4, -6]))
    print(single_num([2, 2, 3, 3, 4, 4, -6, -7]))
