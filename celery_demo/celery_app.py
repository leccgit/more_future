from celery import Celery
from setting import Config

celery_app = Celery(
    "celery_demo",
    broker=Config.BACKEND_URL_BY_REDIS,
    backend=Config.BACKEND_URL_BY_REDIS,
    # include: 每个worker应该导入的模块列表，以实例创建的模块的目录作为起始路径
    include=[
        "src.celery_tasks.task_with_hello",
        "src.celery_tasks.task_with_mg",
    ]
)

# celery更新配置操作
celery_app.conf.update(
    result_expires=3600,  # 设置结果的过期时间
)
if __name__ == '__main__':
    # celery -A celery_operate worker --loglevel=info
    # 注意, 在ide中运行的时候, 存在由于运行参数配置问题, 导致无法运行的情况, 需要编辑 run/Edit相关内容
    celery_app.start()
