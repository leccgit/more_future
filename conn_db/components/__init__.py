from enum import Enum, unique
from typing import Dict, Type

from app.core.components.base_interfaces import DatabaseInterface
from app.core.components.core_mysql import AsyncMysqlCore
from app.core.components.core_redis import AsyncRedisCore


@unique
class MICROTaskKey(Enum):
    aio_mysql = 10
    aio_postgresql = 20
    aio_redis = 30


MICRO_TASKS: Dict[MICROTaskKey, Type[DatabaseInterface]] = {
    MICROTaskKey.aio_mysql: AsyncMysqlCore,
    MICROTaskKey.aio_redis: AsyncRedisCore,
}
