import time

from celery_operate import celery_app


@celery_app.task
def send_celery_msg(name):
    print("向%s发送消息..." % name)
    time.sleep(5)
    print("向%s发送消息完成" % name)
    return "ok"
