import asyncio


async def core(seq) -> list:
    await asyncio.sleep(max(seq))
    print("is in core")
    return list(reversed(seq))


async def main():
    """
    如果在main()中不await t，它可能在main()表明它已完成之前完成(没有执行)。
    由于asyncio.run(main())调用loop.run_until_complete(main())事件循环只关心（没有await t）main()的完成，
    而不是在main()中创建的任务的完成，无需await t，循环的其他任务可能在完成之前会被取消。
    如果您需要获取当前待处理任务的列表，您可以使用asyncio.Task.all_tasks()。
    :return:
    """
    t = asyncio.create_task(core([3, 2, 1]))
    # await t
    print(f't: type {type(t)}')
    print(f't done: {t.done()}')
    print(asyncio.all_tasks())


if __name__ == '__main__':
    asyncio.run(main())
