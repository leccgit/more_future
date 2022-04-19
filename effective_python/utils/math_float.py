from decimal import Decimal


def is_positive_decimal(value) -> Decimal:
    try:
        value = Decimal(str(value))
    except Exception:
        raise ValueError("%s must be an integer or float" % (value,))
    return value


def to_decimal(val) -> Decimal:
    return is_positive_decimal(val)


def to_float(val) -> float:
    if not val:
        return 0
    return float(to_decimal(val))


def float_multi(a, b) -> float:
    return to_float(to_decimal(a) * to_decimal(b))


def float_sum(a, b) -> float:
    return to_float(to_decimal(a) + to_decimal(b))


if __name__ == '__main__':
    import json

    assert to_float(0.01) == 0.01
    assert to_float("0.01") == 0.01

    assert float_sum("0.1", 0.2) == 0.3
    assert float_sum(0.1, 0.2) == 0.3
    assert float_sum("0.1", "0.2") == 0.3

    assert float_multi(0.1, 0.2) == 0.02
    assert float_multi("0.1", 0.2) == 0.02
    assert float_multi("0.1", "0.2") == 0.02

    print(json.dumps({
        "a": float_sum(0.1, 0.2)
    }))
    assert float_multi("0.1000000222", 0.12) == 0.012000002664
    assert float_multi("0.1000000222", 0.000) == 0
