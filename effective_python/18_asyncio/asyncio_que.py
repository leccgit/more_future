import asyncio
from asyncio import Queue

if __name__ == '__main__':
    # async def wait_future():
    #     a_future = asyncio.Future()
    #     print("in wait future!")
    #     await a_future
    #     print("this is end!")

    async def que_put(c_que):
        for i in range(5):
            await c_que.put(i)
            print('[{}]: put with wait!'.format(i))
            rs = await c_que.get()
            print("[{}]: result is {}".format(i, rs))
        print('111')


    # async def que_get(c_que):
    #     for i in range(5):
    #         await c_que.get(i)
    #         print('[{}]: get with wait!'.format(i))
    #     print('111')

    current_loop = asyncio.get_event_loop()
    a_que = Queue(maxsize=3)
    current_loop.run_until_complete(que_put(a_que))
    # current_loop.run_until_complete(que_get(a_que))

    current_loop.close()
    print("thread is close!")

