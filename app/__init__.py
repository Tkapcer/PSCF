from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')     

    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Zaloguj się, aby uzyskać dostęp do tej strony.'

    from app.auth.routes import auth
    from app.auth.routes import bp as schedule_bp
    from app.camera.routes import camera
    from app.main.routes import main

    app.register_blueprint(auth)
    app.register_blueprint(camera)
    app.register_blueprint(main)
    app.register_blueprint(schedule_bp)

    return app