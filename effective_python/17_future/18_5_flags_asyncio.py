import asyncio
import os
import sys
import time

import aiohttp

POP20_CC = ('CN IN US ID BR PK NG BD RU JP '
            'MX PH VN ET EG DE IR TR CD FR').split()
BASE_URL = 'http://flupy.org/data/flags'
DEST_DIR = 'downloads/'


def save_flag(img, filename):  # 阻塞型函数，在触发文件保存操作时候，会阻塞整个应用程序
    path = os.path.join(DEST_DIR, filename)
    with open(path, 'wb') as fp:
        fp.write(img * 100)


async def get_flag(cc):
    url = '{}/{cc}/{cc}.gif'.format(BASE_URL, cc=cc.lower())
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.read()
    return result


def show(text):
    print(text, end=' ')
    sys.stdout.flush()


async def download_one(cc):
    image = await get_flag(cc)
    show(cc)

    save_flag(image, cc.lower() + '.gif')


async def download_many(cc_list):
    t0 = time.time()

    all_tasks = [
        download_one(cc)
        for cc in sorted(cc_list)
    ]
    res = await asyncio.gather(*all_tasks)
    elapsed = time.time() - t0
    msg = '\n{} flags downloaded in {:.2f}s'
    print(msg.format(len(res), elapsed))


def run_sync(feature_or_task):
    cur_loop = asyncio.get_event_loop()
    cur_loop.run_until_complete(feature_or_task)
    cur_loop.close()


if __name__ == '__main__':
    run_sync(download_many(POP20_CC))
# fp.write(img * 100) 4.29s
