#!/usr/bin/env python
import sys

import pika
from random import randint
from study_mq.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 显式创建一个扇形交换机, 命名为logs
channel.exchange_declare(
    exchange='topic_logs',
    exchange_type="topic"
)
channel.queue_declare(queue="", exclusive=True)

binding_keys = ["#", "kern.*", "*.critical", "kern.*" "*.critical"]

for i in range(2):
    routing_key = binding_keys[randint(0, len(binding_keys) - 1)]
    channel.queue_bind(exchange='topic_logs',
                       queue="",
                       routing_key=routing_key)
    print("bind routing key:{}".format(routing_key))

print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue="", on_message_callback=callback)
channel.start_consuming()
