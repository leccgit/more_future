#!/usr/bin/env python

import pika
import time
from rabbitmq_st.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()
# 重复申明的队列, 不会重复创建
channel.queue_declare(queue="hello_world", durable=True)


def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    time.sleep(str(body).count(".") * 0.1)
    print(" [X] Done")


channel.basic_qos(prefetch_count=1)  # 通知rabbitmq, 每次只接收一条消息
channel.basic_consume("hello_world", callback, auto_ack=False)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
