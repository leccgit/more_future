#!/usr/bin/env python

import pika

from rabbitmq_st.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
# 重复申明的队列, 不会重复创建
channel.queue_declare(queue="hello_world")


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)


channel.basic_consume("hello_world", callback, auto_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
