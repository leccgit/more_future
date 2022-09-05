import time

from redis import ConnectionPool, Redis


def test_pipe_line(conn: Redis):
    pipeline = conn.pipeline(transaction=False)
    cron_time = time.time()
    pipeline.multi()
    for i in range(10000000):
        pipeline.set(f"keys_test_{i}", str(i))
    pipeline.execute()
    print(f"cost time:{time.time() - cron_time}")


if __name__ == '__main__':
    redis_pool = ConnectionPool(host='127.0.0.1', port=6378, db=0)
    redis_cnn = Redis(connection_pool=redis_pool)
    test_pipe_line(redis_cnn)
    print("end...")
