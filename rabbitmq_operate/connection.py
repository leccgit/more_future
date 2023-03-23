import pika

from rabbitmq_operate.setting import Config

credentials = pika.PlainCredentials(
    username=Config.RABBITMQ_USER_NAME,
    password=Config.RABBITMQ_PASSWORD
)
connection_params = pika.ConnectionParameters(
    host=Config.RABBITMQ_HOST,
    port=Config.RABBITMQ_PORT,
    credentials=credentials
)
