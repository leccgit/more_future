#!/usr/bin/env python
# python -m unittest hello_world/hello_publish.py
import pika

from connection import connection_params

connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

# 申明队列
channel.queue_declare(queue="hello_world")
body_msg = "hello world!"
channel.basic_publish(
    exchange="",
    routing_key="hello_world",
    body=bytes(body_msg, encoding="utf-8")
)
print(" [x] Sent 'Hello World!'")
connection.close()
