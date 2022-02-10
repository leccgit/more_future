#!/usr/bin/env python
import sys

import pika

from rabbitmq_st.study_rabbitmq.connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 显式创建一个扇形交换机, 命名为logs
# 扇形交换机, 顾名思义像扇子一样, 将消息推送到所有与之绑定的队列中
channel.exchange_declare(
    exchange='pub_logs',
    exchange_type="fanout"
)
body_msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(
    exchange="pub_logs",
    routing_key="",
    body=bytes(body_msg, encoding="utf-8")
)
print(" [x] Sent {}".format(body_msg))
connection.close()
