from typing import Dict, Union

import asyncpg
from pydantic import BaseModel

from conn_db.components.base_interfaces import DatabaseInterface


class PostgreSqlPoolConf(BaseModel):
    """postgresql连接池配置参数"""
    min_size: int = 5
    max_size: int = 20
    max_queries: int = 50000  # 查询数达到该值后, 旧连接将被新连接关闭
    max_inactive_connection_lifetime: float = 300.0  # 非活跃的连接, 达到目标秒数后会被关闭, 值为0将关闭该机制


class PostgreSqlConnConf(BaseModel):
    """postgresql连接参数"""
    hostname: str
    port: int = 5432
    username: str
    password: str
    database: str
    ssl: bool = False
    connection_kwargs: Union[Dict, None] = None

    connection_pool_conf: Union[PostgreSqlPoolConf, None] = None


class AsyncPostgreSqlCore(DatabaseInterface):
    def __init__(self, conn_conf: PostgreSqlConnConf) -> None:
        if conn_conf.connection_pool_conf is None:
            conn_conf.connection_pool_conf = PostgreSqlPoolConf()

        self._conn_conf: PostgreSqlConnConf = conn_conf
        self._pool: Union[asyncpg.Pool, None] = None

    def _get_connection_kwargs(self) -> dict:
        tmp_conn_kws = {
            **self._conn_conf.connection_pool_conf.dict()
        }
        if self._conn_conf.connection_kwargs:
            tmp_conn_kws.update(self._conn_conf.connection_kwargs)

        conn_kwargs = {}
        for key, val in tmp_conn_kws.items():
            # 转换参数保持和连接池中的参数一致
            if key == "minsize":
                key = "min_size"
            elif key == "maxsize":
                key = "max_size"
            conn_kwargs[key] = val
        return conn_kwargs

    async def connect(self):
        assert self._pool is None, "AsyncPostgreSqlCore is already running"
        kwargs = self._get_connection_kwargs()
        self._pool = await asyncpg.create_pool(
            host=self._conn_conf.hostname,
            port=self._conn_conf.port or 5432,
            user=self._conn_conf.username,
            password=self._conn_conf.password,
            database=self._conn_conf.database,
            **kwargs,
        )

    async def disconnect(self):
        assert self._pool is not None, "AsyncPostgreSqlCore is not running"
        await self._pool.close()
        self._pool = None

    async def acquire_pool(self) -> asyncpg.Connection:
        assert self._pool is not None, "AsyncPostgreSqlCore is not running"
        async with self._pool.acquire() as conn:
            # ps: 该处的上下文管理器, 会将空闲的连接放回连接池而不是断开
            yield conn

    def connection_pool(self) -> asyncpg.Pool:
        return self._pool
