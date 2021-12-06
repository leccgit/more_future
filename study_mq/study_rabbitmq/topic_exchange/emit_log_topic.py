#!/usr/bin/env python
import pika

from study_mq.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 显式创建一个扇形交换机, 命名为logs
# 扇形交换机, 顾名思义像扇子一样, 将消息推送到所有与之绑定的队列中
channel.exchange_declare(
    exchange='topic_logs',
    exchange_type="topic"
)
# 指明发布日志所对应的级别
body_msg = 'Hello World!'
channel.basic_publish(
    exchange="topic_logs",
    routing_key="kern.critical.critical",
    body=bytes(body_msg, encoding="utf-8")
)
print(" [{}] Sent {}".format("kern.critical", body_msg))
connection.close()
