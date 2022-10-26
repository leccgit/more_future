from threading import RLock, Thread, get_ident

g_sum_result = 0


def test_sum_1():
    global g_sum_result
    me = get_ident()
    print("test_sum_1:{}".format(me))
    with RLock():
        for i in range(1000000):
            g_sum_result += 1
    return g_sum_result


def test_sum_2():
    global g_sum_result
    me = get_ident()
    print("test_sum_2:{}".format(me))
    with RLock():
        for i in range(1000000):
            g_sum_result += 1
    return g_sum_result


if __name__ == '__main__':
    thread_sum_1 = Thread(target=test_sum_1, name="test_sum_1")
    thread_sum_2 = Thread(target=test_sum_2, name="test_sum_2")
    thread_sum_1.start()
    thread_sum_1.join()
    thread_sum_2.start()
    thread_sum_2.join()
    print(g_sum_result)
    print(g_sum_result)
