import pika

from rabbitmq_st.study_rabbitmq.setting import Config

rabbitmq_config = Config()

credentials = pika.PlainCredentials(
    username=rabbitmq_config.RABBITMQ_USER_NAME,
    password=rabbitmq_config.RABBITMQ_PASSWORD
)
connection_params = pika.ConnectionParameters(
    host=rabbitmq_config.RABBITMQ_HOST,
    port=rabbitmq_config.RABBITMQ_PORT,
    credentials=credentials
)
