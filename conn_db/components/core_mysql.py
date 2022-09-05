from typing import Dict, Union

import aiomysql
from pydantic import BaseModel

from conn_db.components.base_interfaces import DatabaseInterface

ONE_HOUR = 60 * 60


class MysqlPoolConf(BaseModel):
    """mysql连接池配置参数"""
    min_size: int = 1
    max_size: int = 10  # ps: 看源码, max_size貌似不生效 TODO
    echo: bool = True
    pool_recycle: int = 7 * ONE_HOUR  # 连接超时参数, mysql默认超时时间8小时


class MysqlConnConf(BaseModel):
    """mysql连接参数"""
    hostname: str
    port: int = 3306
    username: str
    password: str
    database: str
    ssl: bool = False
    autocommit: bool = True
    charset: str = "utf8"
    connection_kwargs: Union[Dict, None] = None

    connection_pool_conf: Union[MysqlPoolConf, None] = None

    @property
    def engine_url(self):
        return f'mysql+pymysql://{self.username}:{self.password}' \
               f'@{self.hostname}:{self.port}/{self.database}?charset={self.charset}'


class AsyncMysqlCore(DatabaseInterface):
    def __init__(self, conn_conf: MysqlConnConf) -> None:
        if conn_conf.connection_pool_conf is None:
            conn_conf.connection_pool_conf = MysqlPoolConf()

        self._conn_conf: MysqlConnConf = conn_conf
        self._pool: Union[aiomysql.Pool, None] = None

    def _get_connection_kwargs(self) -> dict:
        tmp_conn_kws = {
            **self._conn_conf.connection_pool_conf.dict()
        }
        if self._conn_conf.connection_kwargs:
            tmp_conn_kws.update(self._conn_conf.connection_kwargs)

        conn_kwargs = {}
        for key, val in tmp_conn_kws.items():
            # 转换参数保持和连接池中的参数一致
            if key == "min_size":
                key = "minsize"
            elif key == "max_size":
                key = "maxsize"
            conn_kwargs[key] = val
        return conn_kwargs

    async def connect(self):
        assert self._pool is None, "AsyncMysqlCore is already running"
        kwargs = self._get_connection_kwargs()
        self._pool = await aiomysql.create_pool(
            host=self._conn_conf.hostname,
            port=self._conn_conf.port or 3306,
            user=self._conn_conf.username,
            password=self._conn_conf.password,
            db=self._conn_conf.database,
            autocommit=self._conn_conf.autocommit,
            **kwargs,
        )

    async def disconnect(self):
        assert self._pool is not None, "AsyncMysqlCore is not running"
        self._pool.close()
        await self._pool.wait_closed()
        self._pool = None

    async def acquire_pool(self) -> aiomysql.Connection:
        assert self._pool is not None, "AsyncMysqlCore is not running"
        async with self._pool.acquire() as conn:
            # ps: 该处的上下文管理器, 会将空闲的连接放回连接池而不是断开
            yield conn

    def connection_pool(self) -> aiomysql.Pool:
        return self._pool
