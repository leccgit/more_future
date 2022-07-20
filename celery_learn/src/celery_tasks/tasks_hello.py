import time

from celery_operate import celery_app


@celery_app.task(bind=True, serializer="json")
def send_celery_msg(self, name):
    print("向%s发送消息..." % name)
    time.sleep(5)
    print("向%s发送消息完成" % name)
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    return "ok"


@celery_app.task(bind=True, serializer="json")
def send_celery_msg_exception_with_retry(self, name):
    try:
        print("向%s发送消息..." % name)
        print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
            self.request))
        print(1 / 0)
    except Exception as exc:
        raise self.retry(exc=exc)


@celery_app.task(bind=True, serializer="json", autoretry_for=(Exception,))
def send_celery_msg_with_autoretry_for(self, name):
    print("向%s发送消息..." % name)
    print('Executing task id {0.id}, args: {0.args!r} kwargs: {0.kwargs!r}'.format(
        self.request))
    print(1 / 0)
