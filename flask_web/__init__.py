import os

from flask import Flask


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    if test_config is None:
        # 加载配置
        from flask_web.setting import flask_config
        app.config.from_object(flask_config["default"])
    else:
        # 加载测试配置
        app.config.update(test_config)

    # 确保实例文件夹存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册db连接实例
    from flask_web.db.model_bases import db

    db.init_app(app)

    # 注册蓝图
    from flask_web.service import auth
    app.register_blueprint(auth.auth_app)

    app.add_url_rule("/", endpoint="index")  # 定义主界面
    return app
