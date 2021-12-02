#!/usr/bin/env python

import pika

from study_mq.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 申明队列
channel.queue_declare(queue="hello_world")
for i in range(10):
    body_msg = "{}: hello world!".format(i + 1)
    channel.basic_publish(exchange="", routing_key="hello_world", body=bytes(body_msg, encoding="utf-8"))
print(" [x] Sent 'Hello World!'")
connection.close()
