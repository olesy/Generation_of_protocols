from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_principal import Principal
from flask_security import Security, SQLAlchemyUserDatastore
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
bootstrap = Bootstrap()
csrf = CSRFProtect()
principals = Principal()
security = Security()

def create_app(config = Config):
    app = Flask(__name__)
    app.config.from_object(config)
    #Настройка расширений, что именно для этого сервера мы настраиваем, паттерн фабрики приложений
    db.init_app(app)
    #
    migrate.init_app(app, db)
    login.init_app(app)
    principals.init_app(app)
    security.init_app(app, user_data_store)
    #auth - настройка маршрута (blue_print). Для построения архитектуры. поключаемся login_manager, куда будем переключаться, если нет прав на страницу
    #Если не заругистрирован, то будет перебрасывать на логин
    app.login_manager.login_view = "auth.login"

    csrf.init_app(app)
    bootstrap.init_app(app)
    from app.home import bp as home_bp
    app.register_blueprint(home_bp)

    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from app.profile import bp as profile_bp
    app.register_blueprint(profile_bp)

    from app.student_handler import bp as student_handler_bp
    app.register_blueprint(student_handler_bp)

    return app

#запускаем init.py
from app import models
user_data_store = SQLAlchemyUserDatastore(db, models.User, models.Role)
