
from __future__ import absolute_import, unicode_literals

from celery import Celery

from setting import Config

app = Celery(
    "celery_01",
    broker=Config.REMOTE_RABBIT_MQ_BROKER_URL,
    backend=Config.REMOTE_MONGO_BACKEND_URL,
    # include=['01_celery']
)
app.conf.update(
    result_expires=3600,
)
if __name__ == '__main__':
    # celery -A celery_hello.celery_01 worker --loglevel=info
    app.start()
