import threading
from flask import Flask, _request_ctx_stack

app = Flask(__name__)
# 先观察_request_ctx_stack中包含的信息
print(_request_ctx_stack._local._storage.storage)


# 创建一个函数，用于向栈中推入请求上下文
# 本例中不使用`with`语句
def worker():
    # 使用应用的test_request_context()方法创建请求上下文
    request_context = app.test_request_context()
    with request_context:
        print('打印堆栈信息: {}'.format(_request_ctx_stack._local._storage.storage))


# 创建3个进程分别执行worker方法
for i in range(3):
    t = threading.Thread(target=worker)
    t.start()
print(_request_ctx_stack._local._storage.storage)
