#!/usr/bin/env python

import pika
from random import randint
from study_mq.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 显式创建一个扇形交换机, 命名为logs
channel.exchange_declare(
    exchange='direct_logs',
    exchange_type="direct"
)
channel.queue_declare(queue="", exclusive=True)

log_level = ["debug", "info", "error"]
for i in range(2):
    routing_key = log_level[randint(0, len(log_level) - 1)]
    channel.queue_bind(
        queue="",
        exchange="direct_logs",
        routing_key=routing_key
    )
    print("bind routing key:{}".format(routing_key))
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue="", on_message_callback=callback)
channel.start_consuming()
