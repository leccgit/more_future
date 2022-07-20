import os
from dotenv import load_dotenv

# 获取配置环境路径
basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, ".env"))


# 基础配置参数
class Config(object):
    REMOTE_IP = os.environ.get("REMOTE_IP")
    REMOTE_RABBIT_MQ_BROKER_URL = os.environ.get("REMOTE_RABBIT_MQ_BROKER_URL")
    REMOTE_REDIS_BACKEND_URL = os.environ.get("REMOTE_REDIS_BACKEND_URL")
    REMOTE_MONGO_BACKEND_URL = os.environ.get("REMOTE_MONGO_BACKEND_URL")


if __name__ == '__main__':
    print(basedir)
    print(os.path.join(basedir, ".env"))
    print(Config.REMOTE_IP)
    assert Config.REMOTE_IP is not None, "please check .env!"
