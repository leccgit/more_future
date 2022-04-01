# !/usr/bin/env python
import pika

from rabbitmq_st.rabbitmq_demo.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

channel.queue_declare(queue="rpc_queue")


def fib(n):
    # print(fib_iter(100)) # => 354224848179261915075
    assert n >= 0, '{} must be positive integer'.format(n)
    if n <= 1:
        return n
    fb1 = 0
    fb2 = 1
    for _ in range(n - 1):
        sum_fb = fb1 + fb2
        fb1 = fb2
        fb2 = sum_fb
    return fb2


def on_request(ch, method, props, body):
    try:
        if type(body) == bytes:
            body = body.decode("utf-8") or 0
        n = int(body)
        print(" [.] fib(%s)" % (n,))
    except Exception as e:
        print(e)
        raise
    response = fib(n)
    # 该处, 也是有可能抛出异常
    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue="rpc_queue", on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
