import time
import threading

globals_set_value_1 = 0
globals_set_value_2 = 0


def thread_a_set_value():
    global globals_set_value_1
    global globals_set_value_2

    thread_a_lock = threading.Lock()
    thread_a_lock.acquire()
    globals_set_value_1 = 'a'
    thread_a_lock.acquire()
    time.sleep(.5)
    # thread_a_lock.release()
    #
    # thread_a_lock.acquire()
    globals_set_value_2 = 'a'
    thread_a_lock.release()


def thread_b_set_value():
    global globals_set_value_1
    global globals_set_value_2

    thread_b_lock = threading.Lock()
    thread_b_lock.acquire()
    globals_set_value_2 = 'b'
    time.sleep(.5)
    # thread_b_lock.release()
    #
    # thread_b_lock.acquire()
    globals_set_value_2 = 'b'
    thread_b_lock.release()


if __name__ == '__main__':
    thread_a_set_value()
    thread_b_set_value()
    print(globals_set_value_1, globals_set_value_2)
    print('end!')
