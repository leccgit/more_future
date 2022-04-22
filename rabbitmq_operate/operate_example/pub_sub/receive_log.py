#!/usr/bin/env python

import pika

from connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 显式创建一个扇形交换机, 命名为logs
channel.exchange_declare(
    exchange='pub_logs',
    exchange_type="fanout"
)
# exclusive: 创建一个临时的队列，程序解释即删除该队列
# queue: 空字符串，则rabbitmq会系统规则创建队列名称
result = channel.queue_declare("", exclusive=True)
que_name = result.method.queue
channel.queue_bind(queue=que_name, exchange="pub_logs")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


print(' [*] Waiting for messages. To exit press CTRL+C')
channel.basic_consume(queue=que_name, on_message_callback=callback)
channel.start_consuming()
