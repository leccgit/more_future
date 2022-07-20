import time
from celery import Celery

from celery_conf import Config

app = Celery(
    "celery_learn",
    broker=Config.REMOTE_RABBIT_MQ_BROKER_URL,
    backend=Config.REMOTE_MONGO_BACKEND_URL,
    # include: 每个worker应该导入的模块列表，以实例创建的模块的目录作为起始路径
    include=["src.celery_hello.celery_to_hello"]
)

app.conf.update(
    result_expires=3600,
)


@app.task
def send_msg(name):
    print("向%s发送消息..." % name)
    time.sleep(5)
    print("向%s发送消息完成" % name)
    return "ok"


if __name__ == '__main__':
    # celery -A src.celery_hello.celery_to_hello worker --loglevel=info
    # 注意, 在ide中运行的时候, 存在由于运行参数配置问题, 导致无法运行的情况, 需要编辑 run/Edit相关内容
    app.start()
