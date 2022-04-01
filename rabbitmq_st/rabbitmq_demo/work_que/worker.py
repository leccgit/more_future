#!/usr/bin/env python

import pika
import time

from connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
# 重复申明的队列, 不会重复创建
channel.queue_declare(queue="hello_world", durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(str(body).count(".") * .1)
    print(" [X] Done")
    # 注意：在rabbitmq中，如果发出的消息，得不到确认，那么该条消息会在rabbitmq中挤压导致rabbitmq的内存占用率越来越高
    ch.basic_ack(delivery_tag=method.delivery_tag)


# 通知rabbitmq, 该消费者每次只处理一条消息，注意可能导致rabbitmq的队列被填满，需按工作场景选择合适的策略
channel.basic_qos(prefetch_count=1)
channel.basic_consume("hello_world", callback)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
