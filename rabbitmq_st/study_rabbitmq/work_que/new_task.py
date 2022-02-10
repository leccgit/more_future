#!/usr/bin/env python

import pika

from random import randint
from rabbitmq_st.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 申明队列, durable=True将队列声明为持久化, 否则rabbitmq
# 注意, 针对rabbitmq的消息持久化, 并不是绝对的, 消息保存在缓存中并不是实时写入到硬盘内的
channel.queue_declare(queue="hello_world", durable=True)
for idx, i in enumerate(range(0, 10), 1):
    body_msg = str(idx) + "." * randint(20, 50)
    channel.basic_publish(
        exchange="",
        routing_key="hello_world",
        body=bytes(body_msg, encoding="utf-8"),
        properties=pika.BasicProperties(
            delivery_mode=2,  # 消息持久化
        )
    )
    print(" [{}] Sent '{}'".format(idx, body_msg))
connection.close()
