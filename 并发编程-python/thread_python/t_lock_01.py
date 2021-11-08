from threading import Thread, Lock, get_ident

g_sum_result = 0
g_lock = Lock()


def test_sum_1():
    global g_sum_result, g_lock
    me = get_ident()
    print("test_sum_1:{}".format(me))
    g_lock.acquire()
    for i in range(1000000):
        g_sum_result += 1
    g_lock.release()
    print("sum1_result:{}".format(g_sum_result))
    return g_sum_result


def test_sum_2():
    global g_sum_result, g_lock
    me = get_ident()
    print("test_sum_2:{}".format(me))
    g_lock.acquire()
    for i in range(1000000):
        g_sum_result += 1
    g_lock.release()
    print("sum2_result:{}".format(g_sum_result))
    return g_sum_result


if __name__ == '__main__':
    thread_sum_1 = Thread(target=test_sum_1, name="test_sum_1")
    thread_sum_2 = Thread(target=test_sum_2, name="test_sum_2")
    thread_sum_1.start()
    thread_sum_1.join()
    thread_sum_2.start()
    thread_sum_2.join()
