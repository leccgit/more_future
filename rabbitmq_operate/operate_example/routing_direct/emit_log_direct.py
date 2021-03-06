#!/usr/bin/env python
import sys
import pika
from random import randint

from connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 创建一个直连交换机
channel.exchange_declare(
    exchange='direct_logs',
    exchange_type="direct"
)
# 指明发布日志所对应的级别
log_level = ["debug", "info", "error"]
severity = log_level[randint(0, len(log_level) - 1)]
body_msg = ' '.join(sys.argv[1:]) or "info: Hello World!"
channel.basic_publish(
    exchange="direct_logs",
    routing_key=severity,
    body=bytes(body_msg, encoding="utf-8")
)
print(" [{}] Sent {}".format(severity, body_msg))
connection.close()
