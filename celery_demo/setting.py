import os

from dotenv import load_dotenv

# 获取配置环境路径
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


# 基础配置参数
class Config(object):
    BROKER_URL_BY_RABBITMQ = os.environ.get("BROKER_URL_BY_RABBITMQ")
    BACKEND_URL_BY_REDIS = os.environ.get("BACKEND_URL_BY_REDIS")
    BACKEND_URL_BY_MONGO = os.environ.get("BACKEND_URL_BY_MONGO")
