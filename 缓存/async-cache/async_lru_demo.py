import aiohttp
import asyncio

from async_lru import alru_cache

"""
    异步: alru_cache缓存
    lru简单原理伪代码:
        lru_cache = {}
        if key not in lru_cache:
            lru_cache[key] = value # key 需要具有唯一性, 一般会对key进行hash处理
        return lru_cache[key]
    ps: 使用lru的, 一般为不易发生变动的数据, 需要经常变动的数据不适合使用lru
    demo链接: https://github.com/aio-libs/async-lru
"""


@alru_cache(maxsize=32)
async def get_pep(num):
    resource = 'http://www.python.org/dev/peps/pep-%04d/' % num
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(resource) as s:
                return await s.read()
        except aiohttp.ClientError:
            return 'Not Found'


async def main():
    for n in 8, 290, 308, 320, 8, 218, 320, 279, 289, 320, 9991:
        pep = await get_pep(n)
        print(n, len(pep))

    print(get_pep.cache_info())
    # CacheInfo(hits=3, misses=8, maxsize=32, currsize=8)

    # closing is optional, but highly recommended
    await get_pep.close()


loop = asyncio.get_event_loop()

loop.run_until_complete(main())

loop.close()
