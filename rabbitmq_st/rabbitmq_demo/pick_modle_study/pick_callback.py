"""
    pika: 使用回调传递的风格连接到rabbitmq
"""
import pika

from rabbitmq_st.rabbitmq_demo.connection import connection_params


def on_open(mq_connection):
    mq_connection.channel(on_open_callback=on_channel_open)


def on_channel_open(mq_channel):
    mq_channel.exchange_declare(
        exchange='pub_logs',
        exchange_type="fanout"
    )
    mq_channel.basic_publish(
        exchange="pub_logs",
        routing_key="",
        body='Test Message',
        properties=pika.BasicProperties(
            content_type='text/plain',
            type='example'
        ))
    print(" [x] Sent {}".format("Test Message"))


connection = pika.SelectConnection(parameters=connection_params, on_open_callback=on_open)

try:
    # Step #2 - Block on the IOLoop
    connection.ioloop.start()

# Catch a Keyboard Interrupt to make sure that the connection is closed cleanly
except KeyboardInterrupt:

    # Gracefully close the connection
    connection.close()

    # Start the IOLoop again so Pika can communicate, it will stop on its own when the connection is closed
    connection.ioloop.start()
