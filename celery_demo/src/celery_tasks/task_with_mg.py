import asyncio
from threading import RLock

from celery.utils.log import get_task_logger
from celery_app import celery_app
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient

logger = get_task_logger(__name__)


class IdiHandleBasicStore:
    @property
    def client_host(self):
        return "127.0.0.1"

    @property
    def client_port(self):
        return 27017

    @classmethod
    def retry_interval(cls):
        return 5

    def create_handle(self) -> MongoClient:
        raise NotImplemented


class MotorHandleStore(IdiHandleBasicStore):
    def create_handle(self) -> AsyncIOMotorClient:
        return AsyncIOMotorClient(
            self.client_host, self.client_port
        )


class Context:
    _db_context = {}  # 内存中的db
    _lock = RLock()

    @classmethod
    def init_db_context(cls):
        if not cls._db_context.get("mongo_client"):
            cls._db_context["mongo_client"] = MotorHandleStore().create_handle()
            logger.info("create mongo client suc...")
        return cls._db_context["mongo_client"]

    @classmethod
    def get_db_context(cls):
        with cls._lock:
            if not cls._db_context.get("mongo_client"):
                cls.init_db_context()
            return cls._db_context["mongo_client"]


##################
# celery task
##################

@celery_app.task
def compute_process_single_with_celery():
    Context.init_db_context()
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(get_result())
    return result


async def get_result():
    handler = Context.get_db_context()
    operate_db = handler['idi_{}'.format("xddq")]
    collection = operate_db["xddq_context_cache"]

    result = await collection.find_one({
        "code": "iot_device_status_cfg"
    }, {"_id": 0})
    logger.info("=" * 20)
    logger.info("result:{}".format(result))

    return result
