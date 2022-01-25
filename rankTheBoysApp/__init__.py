
from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from rankTheBoysApp.config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from rankTheBoysApp.users.routes import users
    from rankTheBoysApp.pools.routes import thePools
    from rankTheBoysApp.main.routes import main
    from rankTheBoysApp.errors.handlers import errors

    app.register_blueprint(errors)
    app.register_blueprint(users)
    app.register_blueprint(thePools)
    app.register_blueprint(main)

    return app