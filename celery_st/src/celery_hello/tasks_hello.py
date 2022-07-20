from __future__ import absolute_import, unicode_literals

from .celery_01 import app


@app.task
def add(x, y):
    return x + y


@app.task
def mul(x, y):
    return x * y


@app.task
def xsum(numbers):
    return sum(numbers)


if __name__ == '__main__':
    import time
    res = add.delay(2, 3)
    time.sleep(4)
    print(res.get(timeout=1))
