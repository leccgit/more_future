# 全排列问题
"""
result = []
def backtrack(路径, 选择列表):
    if 满足结束条件:
        result.add(路径)
        return

    for 选择 in 选择列表:
        做选择
        backtrack(路径, 选择列表)
        撤销选择
"""
from typing import Callable


def permutation(nums: list, traceback_func: Callable):
    result = []
    traceback_func(nums, track=[], track_len=len(nums), res=result)
    return result


def fi_traceback(nums: list, track: list, track_len: int, res: list):
    if len(track) == track_len:
        res.append(''.join([str(s) for s in track]))
        return
    for n in nums:
        if n in track:
            continue
        track.append(n)
        fi_traceback(nums, track, track_len, res)
        track.pop()


def se_traceback(nums: list, track: list, track_len: int, res: list):
    if len(track) == track_len:
        res.append(''.join([str(s) for s in track]))
        return
    for idx, n in enumerate(nums):
        if n in track:
            continue
        track.append(n)
        se_traceback([k for _id, k in enumerate(nums) if _id != idx], track, track_len, res)
        track.pop()


if __name__ == '__main__':
    from time import time
    from itertools import permutations

    # start_time = time()
    # fir_result = permutation(list(range(1, 9)), traceback_func=fi_traceback)
    # end_time = time()
    # print("cost time is:{}".format(end_time - start_time))
    # se_result = permutation(list(range(1, 9)), traceback_func=se_traceback)
    # print("cost time is:{}".format(time() - end_time))

    s_time = time()
    _p_result = permutations(list(range(1, 10)))
    p_result = []
    for data in _p_result:
        p_result.append(''.join([str(n) for n in data]))
    print("cost time is:{}".format(time() - s_time))
    # assert fir_result == se_result, "func check error!"
