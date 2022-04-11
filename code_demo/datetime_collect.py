from typing import Tuple

_DAYS_IN_MONTH = [-1, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def _is_leap(year: int):
    # 判断当前的年份是否为润年
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year: int, month: int) -> int:
    # 获取当前年份所在月份的天数
    assert 1 <= month <= 12, month
    if month == 2 and _is_leap(year):
        return 29
    return _DAYS_IN_MONTH[month]


def next_month(year: int, month: int) -> Tuple[int, int]:
    if not 1 <= month <= 12:
        raise ValueError('month must be in 1..12', month)
    if month == 12:
        year += 1
        month = 1
    return year, month
