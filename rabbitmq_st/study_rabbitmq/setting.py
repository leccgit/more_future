import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


class Config(object):
    RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
    RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
    RABBITMQ_USER_NAME = os.environ.get("RABBITMQ_USER_NAME")
    RABBITMQ_PASSWORD = os.environ.get("RABBITMQ_PASSWORD")
