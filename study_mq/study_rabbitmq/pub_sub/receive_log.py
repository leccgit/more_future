#!/usr/bin/env python

import pika
from study_mq.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 显式创建一个扇形交换机, 命名为logs
channel.exchange_declare(
    exchange='pub_logs',
    exchange_type="fanout"
)
channel.queue_declare(queue="", exclusive=True)
channel.queue_bind(queue="", exchange="pub_logs")
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume(queue="", on_message_callback=callback)
channel.start_consuming()
