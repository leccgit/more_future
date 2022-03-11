#!/usr/bin/env python

import pika
from random import randint

from connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 创建一个直连交换机
channel.exchange_declare(
    exchange='direct_logs',
    exchange_type="direct"
)
result = channel.queue_declare(queue="", exclusive=True)
que_name = result.method.queue

print("create que name: {}".format(que_name))

log_level = ["debug", "info", "error"]
for i in range(2):
    routing_key = log_level[randint(0, len(log_level) - 1)]
    channel.queue_bind(
        queue=que_name,
        exchange="direct_logs",
        routing_key=routing_key
    )
    print("bind routing key:{}".format(routing_key))
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue=que_name, on_message_callback=callback)
channel.start_consuming()
