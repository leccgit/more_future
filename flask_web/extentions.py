# 扩展模块。每个扩展都是在位于app.py中的app工厂中初始化的
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt

csrf_protect = CSRFProtect()
login_manager = LoginManager()
db = SQLAlchemy()
bcrypt = Bcrypt()
