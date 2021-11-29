## 1. python asyncio

### 1.1 异步版本

```python
import asyncio


async def count():
    print("one")
    # ps: time.sleep() 会堵塞住线程, 在该处只能使用异步版本
    await asyncio.sleep(1)
    print("two")


async def main():
    await asyncio.gather(*[count(), count(), count()])


if __name__ == '__main__':
    current_loop = asyncio.get_event_loop()
    result = current_loop.run_until_complete(main())
    current_loop.close()
```

### 1.2 同步版本

```python
import time


def count():
    print("one")
    time.sleep(1)
    print("two")


def main():
    for _ in range(3):
        count()


if __name__ == '__main__':
    main()
```