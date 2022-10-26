from typing import Dict, Union

from pydantic import BaseModel
from redis import asyncio as aioredis

from db_connection.components.base_interfaces import DatabaseInterface


class RedisPoolConf(BaseModel):
    max_connections: int = 50  # 连接池的最大连接数
    decode_responses: bool = True  # 是否解析响应数据, 默认为False返回byte
    health_check_interval: int = 0


class RedisConf(BaseModel):
    hostname: str
    port: int = 6379
    database: int = 0
    username: str
    password: str
    connection_kwargs: Union[Dict, None] = None
    connection_pool_conf: Union[RedisPoolConf, None] = None


class AsyncRedisCore(DatabaseInterface):
    def __init__(self, conn_conf: RedisConf) -> None:
        if conn_conf.connection_pool_conf is None:
            conn_conf.connection_pool_conf = RedisPoolConf()

        self._conn_conf: RedisConf = conn_conf
        self._pool: Union[aioredis.ConnectionPool, None] = None

    def _get_connection_kwargs(self) -> dict:
        conn_kwargs = {
            **self._conn_conf.connection_pool_conf.dict()
        }
        if self._conn_conf.connection_kwargs:
            conn_kwargs.update(self._conn_conf.connection_kwargs)

        return conn_kwargs

    async def connect(self):
        assert self._pool is None, "AsyncRedisCore is already running"
        kwargs = self._get_connection_kwargs()
        self._pool = aioredis.ConnectionPool(
            host=self._conn_conf.hostname,
            port=self._conn_conf.port or 6379,
            db=self._conn_conf.database or 0,
            username=self._conn_conf.username,
            password=self._conn_conf.password,
            **kwargs,
        )

    async def disconnect(self):
        assert self._pool is not None, "AsyncRedisCore is not running"
        await self._pool.disconnect()
        self._pool = None

    async def acquire_pool(self) -> aioredis.Redis:
        assert self._pool is not None, "AsyncRedisCore is not running"
        return aioredis.Redis(connection_pool=self._pool)

    def connection_pool(self) -> aioredis.ConnectionPool:
        return self._pool
