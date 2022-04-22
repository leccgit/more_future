#!/usr/bin/env python

import pika

from random import randint
from rabbitmq_operate.operate_example.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 申明队列, durable=True 将队列声明为持久化, 否则rabbitmq重启后将会删除队列
# 持久化消息, delivery_mode=2 将队列中的消息也声明为持久化, 避免rabbitmq重启后的消息丢失
# 注意, 针对rabbitmq的队列/消息的持久化, 并不是绝对的, 消息首先保存在缓存中, 按同步策略写入到硬盘内, 这一点和redis的aof缓冲类似
# 同时, 需要注意已经声明的队列, 在更改为持久化, 是无效的
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
