#!/usr/bin/env python

import pika

from connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
channel.queue_declare(queue="hello_world")  # 接受者也显示的声明这个队列，避免队列没有创建


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


"""
auto_ack:
    basic.ack: 自动肯定确认，消息发送就删除，假定消费者已经成功处理，对于数据不安全，但是能够支持更高的吞吐量
    basic.nack: 否定确认，消息发送失败不会被删除
    basic.reject: 自动否定确认，消息发送就删除，假定消息未处理
ps：如果auto_ack=False，则当callback中运行异常，rabbitmq不会删除该消息
"""
channel.basic_consume("hello_world", callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
