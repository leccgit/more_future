import asyncio
import itertools
import sys

write, flush = sys.stdout.write, sys.stdout.flush


class Signal:
    go = True


async def spin(msg):
    # 模拟打印程序
    status = ""
    for char in itertools.cycle(r"|/-\\"):
        status = f"{char} {msg}"
        write(status)
        flush()
        write('\x08' * len(status))  # 显示文本式动画的诀窍所在：使用退格符（\x08）把光标移回来。
        await asyncio.sleep(.1)
        if not Signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))


async def slow_func(sleep_time=3):
    # 模拟i/o等待
    await asyncio.sleep(sleep_time)
    Signal.go = False
    return 42


async def supervisor():
    result = await asyncio.gather(*[spin("think asyncio"), slow_func()])
    print("supervisor start: ", "*" * 10)
    return result[1]


def main():
    current_loop = asyncio.get_event_loop()
    result = current_loop.run_until_complete(supervisor())
    current_loop.close()
    print('Answer:', result)


if __name__ == '__main__':
    main()
