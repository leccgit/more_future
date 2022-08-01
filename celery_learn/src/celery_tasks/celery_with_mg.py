import asyncio
from celery.utils.log import get_task_logger
from motor.motor_asyncio import AsyncIOMotorClient
from mg_app_framework import set_handler, TaskKey, get_handler, IdiServerConfigBasic

from base_conf import Config
from celery_operate import celery_app

logger = get_task_logger(__name__)


class IdiConfigBasicStore(IdiServerConfigBasic):

    def get_mongodb_host(self):
        return Config.REMOTE_IP

    def get_mongodb_port(self):
        return 27017

    def retry_interval(self):
        return 5


class Context:
    """
    模仿mg context或者handler相关，使用类变量在进程内全局共享，数据库、消息队列、配置等
    在task内部尝试创建连接和处理数据
    这里要记住一点，task都是在单独的进程中执行的，没有什么特别的地方
    """
    _db = None

    @staticmethod
    def init_db_connection():
        if not Context._db:
            logger.info("get_db_connection")
            mongodb_host = IdiConfigBasicStore().get_mongodb_host()
            mongodb_port = int(IdiConfigBasicStore().get_mongodb_port())
            Context._db = AsyncIOMotorClient(
                mongodb_host, mongodb_port
            )
            set_handler(TaskKey.mongodb_async, Context._db)
        return Context._db


##################
# celery task
##################

@celery_app.task
def compute_process_single_with_celery():
    Context.init_db_connection()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_result())
    return result


async def get_result():
    handler = get_handler(TaskKey.mongodb_async)
    operate_db = handler['idi_{}'.format("xddq")]
    collection = operate_db["datas"]

    result = await collection.find_one({
        "code": "device_1_2~zb_r_jslljp"
    }, {"_id": 0})
    logger.info("get_result:{}".format(result))
    print("=" * 20)
    print("result:{}".format(result))

    return result
