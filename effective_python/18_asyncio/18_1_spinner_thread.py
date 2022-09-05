# from concurrent import futures
import itertools
import sys
import threading
import time

write, flush = sys.stdout.write, sys.stdout.flush


class Signal:
    go = True


def spin(msg, signal: Signal):
    # 模拟打印程序
    status = ""
    for char in itertools.cycle(r"|/-\\"):
        status = f"{char} {msg}"
        write(status)
        flush()
        write('\x08' * len(status))  # 显示文本式动画的诀窍所在：使用退格符（\x08）把光标移回来。
        time.sleep(.1)
        if not signal.go:
            break
    write(' ' * len(status) + '\x08' * len(status))


def slow_func(sleep_time=3):
    # 模拟i/o等待
    time.sleep(sleep_time)
    return 42


def supervisor():
    signal = Signal()
    spinner = threading.Thread(target=spin, args=("supervisor-test", signal))
    print("supervisor start: ", "*" * 10)
    spinner.start()
    result = slow_func()  # 调用sleep来阻塞主线程，以便释放gil，创建从属线程
    signal.go = False
    spinner.join()
    return result


def main():
    result = supervisor()
    print('Answer:', result)


if __name__ == '__main__':
    main()
